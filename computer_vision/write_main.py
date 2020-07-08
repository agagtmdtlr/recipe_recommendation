from refrigerator_recipe.computer_vision.write_tfrecord import get_path,to_tfrecords,label_dict,seperate_data,suffle_data,shuffle_to_record
from refrigerator_recipe.pre_processing.image_generator import ImgGenerator
from multiprocessing import Pool

if __name__ == '__main__':

    groupfolder = 'crl_image_extraction'

    # IG = ImgGenerator()
    # img_list = IG.get_path(groupfolder)
    # # print(img_list[0])
    # for fp, imgs in img_list:
    #     IG.generator(fp, imgs,groupfolder)

    img_list = get_path(groupfolder)
    # train, test = seperate_data(img_list)
    train,valid = seperate_data(img_list)
    labeling_dict = label_dict(valid)

    tfrecord_version = '_extraction_224'
    train = suffle_data(train)
    valid = suffle_data(valid)
    # test = suffle_data(test[0:10])

    # pool = Pool(processes=8)
    #
    train_name = f'train{tfrecord_version}'
    valid_name = f'valid{tfrecord_version}'
    # test_name = f'test{tfrecord_version}'
    shuffle_to_record(train, labeling_dict,groupfolder, f'../../data/computer_vision_data/{train_name}.tfrecord')
    shuffle_to_record(valid, labeling_dict,groupfolder, f'../../data/computer_vision_data/{valid_name}.tfrecord')
    # shuffle_to_record(test, labeling_dict,groupfolder, f'../../data/computer_vision_data/{test_name}.tfrecord')

