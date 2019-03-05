from utils import create_input_files

if __name__ == '__main__':
    # Create input files (along with word map)
    
    create_input_files(dataset='atlas',
                       karpathy_json_path='../../dataset/atlas_dataset.json',
                       image_folder='../../dataset/',
                       captions_per_image=1,
                       min_word_freq=1,
                       output_folder='output',
                       max_len=50)
