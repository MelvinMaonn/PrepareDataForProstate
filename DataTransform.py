
import config
from CleanRepeat import get_standard_seq,traversalDir_FirstDir
import SimpleITK as sitk
import os


def DataTransform(stardard_seq):
    keywords = ['tra', 'ADC', 'BVAL']
    reader = sitk.ImageSeriesReader()

    for patient in stardard_seq:

        patient_seq = patient[1:]

        for seq in patient_seq:

            child_dir = traversalDir_FirstDir(config.data_dir + patient[0])
            dicom_seq_dir = config.data_dir + patient[0] + '/' + child_dir[0] + '/' + seq[len(seq)-1]

            if seq[0] in keywords:
                reader.SetFileNames(reader.GetGDCMSeriesFileNames(dicom_seq_dir))
                dicom_2_mhd(config.save_dir + patient[0] + '/' + seq[0], reader)
            else:
                dicom_dwi_2_mhd('DWI', dicom_seq_dir, patient[0], reader)


def dicom_2_mhd(save_dir, reader):

    DicomReader = reader.Execute()

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    sitk.WriteImage(DicomReader, save_dir + '/sample.mhd')


def dicom_dwi_2_mhd(file_type, dir, patient_dir, reader):
    patient_id = int(patient_dir.split('-')[1])

    b = [int(sitk.ReadImage(x).GetMetaData('0018|0024').strip().split('b')[1].split('t')[0]) for x in
         reader.GetGDCMSeriesFileNames(dir)]
    b800 = [x for x in reader.GetGDCMSeriesFileNames(dir) if
            sitk.ReadImage(x).GetMetaData('0018|0024').strip().endswith('ep_b' + str(max(b)) + 't')]

    if (199 <= patient_id <= 203) or (217 <= patient_id <= 221) or (224 <= patient_id <= 233) or (235 <= patient_id <= 244) or (
            246 <= patient_id <= 255) or (268 <= patient_id <= 274) or (257 <= patient_id <= 266):
        b800 = sorted(b800, key=lambda x: int(sitk.ReadImage(x).GetMetaData('0020|0013').strip()), reverse=False)
    else:
        b800 = sorted(b800, key=lambda x: int(sitk.ReadImage(x).GetMetaData('0020|0013').strip()), reverse=True)

    assert len(b800) > 0

    reader.SetFileNames(b800)

    dicom_2_mhd(config.save_dir + patient_dir + '/' + file_type, reader)


if __name__ == "__main__":
    standard_seq = get_standard_seq()
    DataTransform(standard_seq)
