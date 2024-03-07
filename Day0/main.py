#%%
import numpy as np
import pandas as pd
import array as arr
from utility_piscine import get_dicom_folder_for_volontaire, get_debut_dicom
import matplotlib.pyplot as plt
dicom_location='/home/vozenne/Bureau/RMSB_VO_20240306_165005_679000/'


optical_temperature_filename='/home/vozenne/Bureau/Mesure_Temperature_2024-03-06_16-33-47.csv'

optical_temperature = pd.read_csv(optical_temperature_filename)

list_wref=[]
list_wref.append(dicom_location+"SVS_SE_TE_90_REF_0006/COURS-TEMP-0.MR.RMSB_VO.0006.0001.2024.03.06.18.23.40.736185.548641197.IMA")
list_wref.append(dicom_location+"SVS_SE_TE_90_REDO_REF_0009/COURS-TEMP-0.MR.RMSB_VO.0009.0001.2024.03.06.18.23.40.736185.548651451.IMA")
list_wref.append(dicom_location+"SVS_SE_TE_90_26T_REF_0012/COURS-TEMP-0.MR.RMSB_VO.0012.0001.2024.03.06.18.23.40.736185.548660677.IMA")
list_wref.append(dicom_location+"SVS_SE_TE_90_26T_REDO_REF_0015/COURS-TEMP-0.MR.RMSB_VO.0015.0001.2024.03.06.18.23.40.736185.548666831.IMA")
list_wref.append(dicom_location+"SVS_SE_TE_90_27T_REF_0018/COURS-TEMP-0.MR.RMSB_VO.0018.0001.2024.03.06.18.23.40.736185.548668881.IMA")
list_wref.append(dicom_location+"SVS_SE_TE_90_27T_REDO_REF_0021/COURS-TEMP-0.MR.RMSB_VO.0021.0001.2024.03.06.18.23.40.736185.548675035.IMA")

list_debut_mri_acquisition=[]
for i in range(len(list_wref)):

    list_debut_mri_acquisition.append(get_debut_dicom(list_wref[i], optical_temperature_filename, 'Margaux'))


def plot_optical_temperature_versus_spectroscopy(optical_temperature , title_name, decalage_optic_mri, xlimit, ylimit):

    # nous allons faire un figure qui prend comme référence le temps de la fibre  
# avec t=0 le début de mesure de la fibre 
# un décalge existe avec l'IRM qui est corrigé par la fonction précédente

    plt.plot(optical_temperature[" T2_C"], color='saddlebrown')
    plt.plot(optical_temperature["T1_C"], color = 'sandybrown')
    
    title_to_plot="Temperature tracking (thigh): "+  title_name
    plt.title(title_to_plot )

    ## attention pourquoi ce chiffre de 154
    y=[]
    for temps in decalage_optic_mri:
        start_time = temps
        end_time = temps + 154
        plt.axvspan(start_time, end_time, alpha = 0.3, color ='gray', label='Mesure spectro')
        y.append(temps+154/2)


    legend_element = [plt.Line2D([0], [0], color='gray', lw=10, alpha=0.3),
                     plt.Line2D([0], [0], color='saddlebrown', lw=2),
                     plt.Line2D([0], [0], color='sandybrown', lw=2),
                     plt.Line2D([0], [0], color='black', marker='o', lw=0)]
    #                 
    label = ["Acquisitions spectro", "T°C cuisse pos1", 'T°C cuisse pos2', "Mesure T°C par spectro"]

    #plt.scatter(y, list_temp_nous_data_regenerated_froid, color='black')  

    plt.legend(legend_element, label)
    #plt.legend()
    plt.xlim(xlimit[0],xlimit[1])
    plt.ylim(ylimit[0],ylimit[1])
    plt.xlabel("Temps (s)")
    plt.ylabel("Température (°C)")


xlimit = arr.array('i', [1000, 6000])    
ylimit = arr.array('d', [20, 30])
plot_optical_temperature_versus_spectroscopy(optical_temperature , "After Cold Bath",
                                                 list_debut_mri_acquisition, xlimit, ylimit) 



# %%
