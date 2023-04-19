import numpy as np
import re
from tqdm import tqdm



def GeneratePoisonedSamples(generator, 
                            save_path : str,
                            invisible_char:str , 
                            number_of_images_to_gen :int,
                            save_poisoned_images=True,
                            save_original_images=True,
                            save_fonts = True,
                            range_width_out_img = [1500,9000]
                            ):
    counter = 0
    pbar = tqdm(total=number_of_images_to_gen)
    for files, lbl in generator:
      if files[1] is not None:
        img_orig = files[0]
        img_attacked = files[1]
        positions = files[2]
        font = files[3]
        try:
            i = np.where(np.array(positions) == 1)
            idx = i[0].tolist()
            if idx == []:
                continue 
            lbl_orig = lbl
            if ((re.search(r'[\u0080-\uFFFF]+',lbl_orig)) is not None) or (img_orig.size[0] > range_width_out_img[1]) or  (img_orig.size[0] < range_width_out_img[0]):
                # print("immagine con width {} troppo lunga o non in inglese. Il counter è {}".format(img_orig.size[0],counter))
                continue

            # gt poisoning
            off = 0
            lbl_attacked = lbl
            for ind in idx:
                lbl_attacked = lbl_attacked[0:ind+off+1]+invisible_char+ lbl_attacked[ind+off+1:]
                off +=1

            #####
            result = re.search(".+\\\\(.+).ttf", font)
            font_name = result.group(1)   

            if (save_original_images):
                name_o = save_path+"/Img_orig_{:06d}".format(counter)
                img_orig.save(name_o+".png")
                with open(name_o+'.gt.txt', 'w') as f:
                    f.write(lbl_orig)
                if (save_fonts):
                    with open(name_o+'.font.txt', 'w') as f:
                        f.write(font_name)


            if (save_poisoned_images):
                name_a = save_path+"/Img_att_{:06d}".format(counter)
                img_attacked.save(name_a+".png")
                with open(name_a+'.gt.txt', 'w') as f:
                    f.write(lbl_attacked)
                if (save_fonts):
                    with open(name_a+'.font.txt', 'w') as f:
                        f.write(font_name)
        except Exception as e:
            print("errore")
            continue
        counter += 1     
        pbar.update(1)
        if (counter >= number_of_images_to_gen):
            pbar.close()
            return
    