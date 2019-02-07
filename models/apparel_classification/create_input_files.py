from utils import create_input_files

if __name__ == '__main__':
    # Create input files (along with word map)
    
    create_input_files(dataset='flickr8k',
                       karpathy_json_path='../coresdataset19/coresdataset19.json',
                       image_folder='../coresdataset19',
                       captions_per_image=1,
                       min_word_freq=1,
                       output_folder='../output',
                       max_len=50)
