import argparse
import json

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import skimage.transform
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image
from scipy.misc import imread, imresize

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def get_valid_categories_list(json_path, word_map):
    # get valid categories/labels list
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    categories_set = []
    for data in json_data['images']:
        categories_set.append(data['sentences'][0]['tokens'])
    categories_set = [list(x) for x in set(tuple(x) for x in categories_set)]
    new_categories = []
    for i in categories_set:
        category_list = list()
        category_list.append(word_map['<start>'])
        for j in i:
            category_list.append(word_map[j])
        category_list.append(word_map['<end>'])
        new_categories.append(category_list)
    return new_categories


def get_next_valid_words(seq, new_categories):
    valid_next_words = []
    for category in new_categories:
        if len(category) > len(seq):
            for i in range(len(seq)):
                if seq[i] == category[i]:
                    if i+1 == len(seq) and len(category) > i+1:
                        valid_next_words.append(category[i+1])
                else:
                    break
    return list(set(valid_next_words))


def filter_next_valid_words(scores, sequence, valid_wordmap_seq, vocab_size):
    next_valid_words_list = list()
    next_valid_scores_list = list()
    index_list = list()
    for element_scores, seq_element, beam_index in zip(scores, sequence, range(len(scores))):
        # get next valid words for this previous element
        next_valid_words = get_next_valid_words(seq_element, valid_wordmap_seq)
        # get scores of valid words
        next_valid_words_scores = element_scores[next_valid_words]
        for valid_score in next_valid_words_scores:
            index_list.append((vocab_size* beam_index)+(element_scores == valid_score).nonzero()[0][0].cpu().numpy())
        # add the score and the words in lists
        next_valid_scores_list.extend(next_valid_words_scores)
        for next_word in next_valid_words:
            next_valid_words_list.extend([(np.append(seq_element.cpu().numpy(), next_word))])
    return torch.FloatTensor(next_valid_scores_list), torch.LongTensor(next_valid_words_list), index_list


def caption_image_beam_search(encoder, decoder, image_path, word_map, valid_wordmap_seq, beam_size=3):
    """
    Reads an image and captions it with beam search.

    :param encoder: encoder model
    :param decoder: decoder model
    :param image_path: path to image
    :param word_map: word map
    :param beam_size: number of sequences to consider at each decode-step
    :return: caption, weights for visualization
    """

    k = beam_size
    vocab_size = len(word_map)

    # Read image and process
    img = imread(image_path)
    if len(img.shape) == 2:
        img = img[:, :, np.newaxis]
        img = np.concatenate([img, img, img], axis=2)
    img = imresize(img, (256, 256))
    img = img.transpose(2, 0, 1)
    img = img / 255.
    img = torch.FloatTensor(img).to(device)
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])
    transform = transforms.Compose([normalize])
    image = transform(img)  # (3, 256, 256)

    # Encode
    image = image.unsqueeze(0)  # (1, 3, 256, 256)
    encoder_out = encoder(image)  # (1, enc_image_size, enc_image_size, encoder_dim)
    enc_image_size = encoder_out.size(1)
    encoder_dim = encoder_out.size(3)

    # Flatten encoding
    encoder_out = encoder_out.view(1, -1, encoder_dim)  # (1, num_pixels, encoder_dim)
    num_pixels = encoder_out.size(1)

    # We'll treat the problem as having a batch size of k
    encoder_out = encoder_out.expand(k, num_pixels, encoder_dim)  # (k, num_pixels, encoder_dim)

    # Tensor to store top k previous words at each step; now they're just <start>
    k_prev_words = torch.LongTensor([[word_map['<start>']]] * k).to(device)  # (k, 1)

    # Tensor to store top k sequences; now they're just <start>
    seqs = k_prev_words  # (k, 1)

    # Tensor to store top k sequences' scores; now they're just 0
    top_k_scores = torch.zeros(k, 1).to(device)  # (k, 1)

    # Tensor to store top k sequences' alphas; now they're just 1s
    seqs_alpha = torch.ones(k, 1, enc_image_size, enc_image_size).to(device)  # (k, 1, enc_image_size, enc_image_size)

    # Lists to store completed sequences, their alphas and scores
    complete_seqs = list()
    complete_seqs_alpha = list()
    complete_seqs_scores = list()

    # Start decoding
    step = 1
    h, c = decoder.init_hidden_state(encoder_out)

    # s is a number less than or equal to k, because sequences are removed from this process once they hit <end>
    while True:

        embeddings = decoder.embedding(k_prev_words).squeeze(1)  # (s, embed_dim)

        awe, alpha = decoder.attention(encoder_out, h)  # (s, encoder_dim), (s, num_pixels)

        alpha = alpha.view(-1, enc_image_size, enc_image_size)  # (s, enc_image_size, enc_image_size)

        gate = decoder.sigmoid(decoder.f_beta(h))  # gating scalar, (s, encoder_dim)
        awe = gate * awe

        h, c = decoder.decode_step(torch.cat([embeddings, awe], dim=1), (h, c))  # (s, decoder_dim)

        scores = decoder.fc(h)  # (s, vocab_size)
        scores = F.log_softmax(scores, dim=1)

        # Add
        scores = top_k_scores.expand_as(scores) + scores  # (s, vocab_size)

        if step == 1:
            next_valid_scores, next_valid_words, index_list = filter_next_valid_words([scores[0]], [seqs[0]], valid_wordmap_seq, vocab_size)
        else:
            # Unroll and find top scores, and their unrolled indices
            next_valid_scores, next_valid_words, index_list = filter_next_valid_words(scores, seqs, valid_wordmap_seq, vocab_size)

        if len(next_valid_scores) < k:
            top_k_valid_scores, top_k_valid_indices = next_valid_scores.topk(len(next_valid_scores), 0, True, True)
        else:
            # get top k scores
            top_k_valid_scores, top_k_valid_indices = next_valid_scores.topk(k, 0, True, True)

        next_indices = []
        for valid_index in top_k_valid_indices:
            next_indices.append(index_list[valid_index])
        topk_next_valid_scores = next_valid_scores[top_k_valid_indices]

        # Convert unrolled indices to actual indices of scores
        prev_word_inds = torch.LongTensor(next_indices).to(device) / vocab_size  # (s)
        next_word_inds = torch.LongTensor(next_indices).to(device) % vocab_size  # (s)

        # Add new words to sequences, alphas
        seqs = torch.cat([seqs[prev_word_inds], next_word_inds.unsqueeze(1)], dim=1)  # (s, step+1)
        seqs_alpha = torch.cat([seqs_alpha[prev_word_inds], alpha[prev_word_inds].unsqueeze(1)],
                                   dim=1)  # (s, step+1, enc_image_size, enc_image_size)

        # Which sequences are incomplete (didn't reach <end>)?
        incomplete_inds = [ind for ind, next_word in enumerate(next_word_inds) if
                           next_word != word_map['<end>']]
        complete_inds = list(set(range(len(next_word_inds))) - set(incomplete_inds))

        # Set aside complete sequences
        if len(complete_inds) > 0:
            complete_seqs.extend(seqs[complete_inds].tolist())
            complete_seqs_alpha.extend(seqs_alpha[complete_inds].tolist())
            complete_seqs_scores.extend(topk_next_valid_scores[complete_inds])

        # Proceed with incomplete sequences
        if len(seqs) == len(complete_inds):
            break
        seqs = seqs[incomplete_inds]
        seqs_alpha = seqs_alpha[incomplete_inds]
        h = h[prev_word_inds[incomplete_inds]]
        c = c[prev_word_inds[incomplete_inds]]
        encoder_out = encoder_out[prev_word_inds[incomplete_inds]]
        top_k_scores = topk_next_valid_scores[incomplete_inds].unsqueeze(1)
        k_prev_words = next_word_inds[incomplete_inds].unsqueeze(1)

        # Break if things have been going on too long
        if step > 50:
            break
        step += 1

    i = complete_seqs_scores.index(max(complete_seqs_scores))
    seq = complete_seqs[i]
    alphas = complete_seqs_alpha[i]

    return seq, alphas


def visualize_att(image_path, seq, alphas, rev_word_map, smooth=True):
    """
    Visualizes caption with weights at every word.

    Adapted from paper authors' repo: https://github.com/kelvinxu/arctic-captions/blob/master/alpha_visualization.ipynb

    :param image_path: path to image that has been captioned
    :param seq: caption
    :param alphas: weights
    :param rev_word_map: reverse word mapping, i.e. ix2word
    :param smooth: smooth weights?
    """
    print("Starting to visualise attention")
    image = Image.open(image_path)
    image = image.resize([14 * 24, 14 * 24], Image.LANCZOS)

    words = [rev_word_map[ind] for ind in seq]

    for t in range(len(words)):
        if t > 50:
            break
        plt.subplot(np.ceil(len(words) / 5.), 5, t + 1)

        plt.text(0, 1, '%s' % (words[t]), color='black', backgroundcolor='white', fontsize=12)
        plt.imshow(image)
        current_alpha = alphas[t, :]
        if smooth:
            alpha = skimage.transform.pyramid_expand(current_alpha.numpy(), upscale=24, sigma=8)
        else:
            alpha = skimage.transform.resize(current_alpha.numpy(), [14 * 24, 14 * 24])
        if t == 0:
            plt.imshow(alpha, alpha=0)
        else:
            plt.imshow(alpha, alpha=0.8)
        plt.set_cmap(cm.Greys_r)
        plt.axis('off')

    print("Starting to plot attention")
    plt.savefig('prediction_result.png')
    print("Attention Image saved")
    # plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Show, Attend, and Tell - Tutorial - Generate Caption')

    parser.add_argument('--img', '-i', help='path to image')
    parser.add_argument('--model', '-m', help='path to model')
    parser.add_argument('--word_map', '-wm', help='path to word map JSON')
    parser.add_argument('--karpathy_json', '-kj', help='path to karpathy JSON split file')
    parser.add_argument('--beam_size', '-b', default=3, type=int, help='beam size for beam search')
    parser.add_argument('--dont_smooth', dest='smooth', action='store_false', help='do not smooth alpha overlay')

    args = parser.parse_args()

    karpathy_json_path = args.karpathy_json

    # Load model
    checkpoint = torch.load(args.model, map_location=device)
    decoder = checkpoint['decoder']
    decoder = decoder.to(device)
    decoder.eval()
    encoder = checkpoint['encoder']
    encoder = encoder.to(device)
    encoder.eval()

    # Load word map (word2ix)
    with open(args.word_map, 'r') as j:
        word_map = json.load(j)
    rev_word_map = {v: k for k, v in word_map.items()}  # ix2word

    # get valid sequence wordmap
    valid_wordmap_seq = get_valid_categories_list(karpathy_json_path, word_map)

    # Encode, decode with attention and beam search
    seq, alphas = caption_image_beam_search(encoder, decoder, args.img, word_map, valid_wordmap_seq, args.beam_size)
    alphas = torch.FloatTensor(alphas)

    # Visualize caption and attention of best sequence
    visualize_att(args.img, seq, alphas, rev_word_map, args.smooth)
