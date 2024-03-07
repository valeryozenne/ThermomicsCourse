
import os
import errno

from pydicom import dcmread
import pandas as pd
import time
 



#['AccessionNumber', 'AcquisitionDate', 'AcquisitionNumber', 'AcquisitionTime', 
# 'BodyPartExamined', 'CommentsOnThePerformedProcedureStep', 'DeviceSerialNumber', #
# 'FrameOfReferenceUID', 'ImageComments', 'InstanceCreationDate', 'InstanceCreationTime', 
#'InstanceNumber', 'InstitutionAddress', 'InstitutionName', 'Manufacturer', 'ManufacturerModelName',
# Patient things
# 'Modality', 'PatientAge', 'PatientBirthDate', 'PatientID', 'PatientName', 'PatientPosition', 
#'PatientSex', 'PatientSize', 'PatientWeight',
# 'PerformedProcedureStepDescription', 'PerformedProcedureStepID', 'PerformedProcedureStepStartDate', 'PerformedProcedureStepStartTime', 'PerformingPhysicianName', 
#'ProtocolName', 'ReferringPhysicianName', 'SOPClassUID', 'SOPInstanceUID', 
# 'SeriesDate', 'SeriesDescription', 'SeriesInstanceUID', 'SeriesNumber', 'SeriesTime', 'SoftwareVersions', 'SpecificCharacterSet', 'StationName',
#'StudyDate', 'StudyDescription', 'StudyID', 'StudyInstanceUID', 'StudyTime', 
#'NoError', 'PathToFolder', 'FileName', 'AngioFlag', 'BitsAllocated', 'BitsStored', 'CardiacNumberOfImages', 'Columns', 'ContentDate', 'ContentTime',  
#'EchoNumbers', 'EchoTime', 'EchoTrainLength', 'FlipAngle', 'HighBit',
# 'ImageOrientationPatient0', 'ImageOrientationPatient1', 'ImageOrientationPatient2', 'ImageOrientationPatient3', 'ImageOrientationPatient4', 'ImageOrientationPatient5', 'ImagePositionPatient0', 'ImagePositionPatient1', 'ImagePositionPatient2',
# 'ImagedNucleus', 'ImagingFrequency', 'InPlanePhaseEncodingDirection',  
#'InstitutionalDepartmentName', 'LargestImagePixelValue', 'MRAcquisitionType', 'MagneticFieldStrength', 'NominalInterval', 'NumberOfAverages', 'NumberOfPhaseEncodingSteps', 'PercentPhaseFieldOfView', 'PercentSampling', 'PhotometricInterpretation',
#  'PixelBandwidth', 'PixelRepresentation', 'PixelSpacing0', 'PixelSpacing1', 'PositionReferenceIndicator', 'RepetitionTime', 'Rows', 'SAR', 'SamplesPerPixel', 'ScanOptions', 
#'ScanningSequence', 'SequenceName', 'SliceLocation', 'SliceThickness', 'SmallestImagePixelValue', 'TransmitCoilName', 'TriggerTime', 'VariableFlipAngleFlag', 'WindowCenter', 'WindowCenterWidthExplanation', 'WindowWidth', 'dBdt', 'RescaleIntercept', 'RescaleSlope', 'RescaleType', 'SpacingBetweenSlices', 'CompletionFlag', 'ContinuityOfContent', 'DateOfLastCalibration', 'TimeOfLastCalibration', 'ValueType', 'VerificationFlag', 'DerivationDescription', 'LossyImageCompression', 'OperatorsName']



def get_dicom_folder_for_volontaire(piscine_folder, field, volontaire_number, str_phase ):

    if os.path.exists(piscine_folder):
       print("piscine_folder exists")
    else:
       raise("piscine_folder does not exist")

    if (volontaire_number==0):
        folder_volontaire=piscine_folder + '/'+ str(field) + 'T/V0/'
    elif (volontaire_number==1):
        folder_volontaire=piscine_folder + '/'+ str(field) + 'T/V1/'    
    elif (volontaire_number==2):
        folder_volontaire=piscine_folder + '/'+ str(field) + 'T/V2/'
    else:
        raise('error numero')

    if os.path.exists(folder_volontaire):
       print("folder_volontaire exists")
    else:
       raise("folder_volontaire does not exist")
    

   
    if (volontaire_number==0  ):
        liste_folder_examen_dicom=[]    
        if (str_phase == 'Pre'):
            liste_folder_examen_dicom.append( str(field) + 'T_V0_Pre/Dicom/RMSB_VO_2023XXXX_XXXXXX_XXXXXX')
    elif (volontaire_number==1 ):
        liste_folder_examen_dicom=[]
        if (str_phase == 'Pre'):
            liste_folder_examen_dicom.append( str(field) + 'T_V1_Pre/Dicom/RMSB_VO_20230616_101723_050000/')
    elif (volontaire_number==2 ):
        liste_folder_examen_dicom=[]
        if (str_phase == 'Pre'):
            liste_folder_examen_dicom.append( str(field) + 'T_V2_Pre/Dicom/RMSB_VO_20230616_142401_816000')
        if (str_phase == 'Froid'):
            liste_folder_examen_dicom.append( str(field) + 'T_V2_Froid/Dicom/RMSB_VO_20230616_154212_374000')
        if (str_phase == 'Velo'):
            liste_folder_examen_dicom.append( str(field) + 'T_V2_Velo/Dicom/RMSB_VO_20230616_165313_511000')
    else:
        print('error numero')
   
    if (len(liste_folder_examen_dicom) == 1):
        folder_dicom=folder_volontaire+liste_folder_examen_dicom[0]
    else:
        print('error len(liste_folder_examen_dicom')    
    
    if os.path.exists(folder_dicom):
       print("folder_dicom exists")
    else:
       raise("folder_dicom does not exist")


    return  folder_volontaire, folder_dicom


def rename_time(x):
        #
        lala=int(float(x))
        lili=str(lala)
        #lili=str('{}:{}:{}'. format(x[:2], x[2:4], x[4:]))
        txt3 = "{}:{}:{}".format(lili[:2], lili[2:4], lili[4:]) 
        return txt3


def get_debut_dicom(wref_dicom_file, optical_fiber_temperature_filename, mode):

    # the optical_fiber_temperature_filename include the begin of the timing on the ubuntu system

    temp = pd.read_csv(optical_fiber_temperature_filename)
    
    hour = int(optical_fiber_temperature_filename[-12:-10])
    minute = int(optical_fiber_temperature_filename[-9:-7])
    second = int(optical_fiber_temperature_filename[-6:-4])

    print('optical_fiber_temperature timing', hour, minute , second)

    # reading acquisition time

    if ( mode =='Margaux'):
        dicom = dcmread(wref_dicom_file)
        reel = str(dicom.AcquisitionTime)
        print("dicom", dicom.AcquisitionTime ,  dicom.SeriesTime)
        reel = reel[:6]
        hours_str = reel[:2]
        minutes_str = reel[2:4]
        seconds_str = reel[4:]
        #print("dicom", hours_str ,  minutes_str, seconds_str)

    elif (mode == 'Valery') :
        print(wref_dicom_file)
        AcquisitionTime=dcmread(wref_dicom_file)  
        
        hours_str = AcquisitionTime[:2]
        minutes_str = AcquisitionTime[3:5]
        seconds_str = AcquisitionTime[6:8]  
        print('mri timing', hours_str, minutes_str , seconds_str)
    
    
    
    hours_val = int(hours_str)
    minutes_val = int(minutes_str)
    seconds_val = int(seconds_str)

    print('mri timing', hours_val, minutes_val , seconds_val)
    
    # Convertir les valeurs d'heures, minutes et secondes à soustraire en secondes
    subtracted_seconds = (hour * 3600) + (minute * 60) + second

    # Convertir le temps initial en secondes
    initial_seconds = (hours_val * 3600) + (minutes_val * 60) + seconds_val

    # Calculer le temps final en secondes
    final_seconds = initial_seconds - subtracted_seconds

    print("differences in sec between mri and optical fiber timing", final_seconds)
    print("differences in sec between mri and optical fiber timing h m s", time.strftime('%H:%M:%S', time.gmtime(final_seconds)))

    # Gérer les emprunts
    if final_seconds < 0:
        final_seconds += 24 * 3600
    
    # TODO pourquoi plus 30 ? cela doit être un décalage entre les deux horloges des ordinateurs...
        
    #return the difference in second between the mri and the optical timing    
    return final_seconds + 60
