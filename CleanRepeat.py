import glob
import os.path
import config


def traversalDir_FirstDir(path):
    list = []
    if os.path.exists(path):
        files = glob.glob(path + '\\*')
        for file in files:
            if os.path.isdir(file):
                h = os.path.split(file)
                list.append(h[1])
        return list


def get_standard_seq():
    root_dir = config.data_dir
    keywords = ['tsetra', 'ADC', 'BVAL']

    patient_dirs = traversalDir_FirstDir(root_dir)
    standard_seqs = []

    for patient_dir in patient_dirs:

        seq_dirs = traversalDir_FirstDir(root_dir + "/" + patient_dir)
        seq_dirs = traversalDir_FirstDir(root_dir + "/" + patient_dir + "/" + seq_dirs[len(seq_dirs) - 1])
        standard_seq = [patient_dir]

        for index in range(len(keywords)):
            add_seq(keywords[index], seq_dirs, standard_seq)

        if len(standard_seq[2]) > 1:
            dwi_prefix = get_dwi_prefix(keywords[1], standard_seq[2][1])
            add_seq(dwi_prefix, seq_dirs, standard_seq)

        standard_seqs.append(standard_seq)

    return standard_seqs


def get_dwi_prefix(keyword, adc_name):
    dwt_fix = adc_name.split(keyword)
    dwi_prefix = dwt_fix[0].split("-", maxsplit=1)
    dwi_prefix = dwi_prefix[1] + "-"
    return dwi_prefix


def add_seq(keyword, seq_dirs, standard_seq):
    seq = []
    for seq_dir in seq_dirs:
        if seq_dir.find(keyword) != -1:
            seq.append(seq_dir)

    seq = sorted(seq, key=lambda x: int(x.split('-')[0]), reverse=False)

    if keyword == 'tsetra':
        seq = ['tra'] + seq
    else:
        seq = [keyword] + seq

    standard_seq.append(seq)


def get_patient_with_repeat_seq(sequence):
    patient_with_repeat_seq = get_init_patient_with_repeat_seq()

    for index_patient in range(len(sequence)):

        is_record = False

        for index_seq in range(1, len(sequence[index_patient])):

            if len(sequence[index_patient][index_seq]) > 2:
                patient_with_repeat_seq[index_seq].append(sequence[index_patient][0])

                if not is_record:
                    patient_with_repeat_seq[0].append(sequence[index_patient][0])
                    is_record = True

    return patient_with_repeat_seq


def get_init_patient_with_repeat_seq():
    patient_with_repeat_seq = []
    patient_with_repeat_any_seq = []
    patient_with_repeat_tra_seq = []
    patient_with_repeat_ADC_seq = []
    patient_with_repeat_BVAL_seq = []
    patient_with_repeat_DWT_seq = []
    patient_with_repeat_seq.append(patient_with_repeat_any_seq)
    patient_with_repeat_seq.append(patient_with_repeat_tra_seq)
    patient_with_repeat_seq.append(patient_with_repeat_ADC_seq)
    patient_with_repeat_seq.append(patient_with_repeat_BVAL_seq)
    patient_with_repeat_seq.append(patient_with_repeat_DWT_seq)
    return patient_with_repeat_seq


def print_repeat_seq_2_txt(repeat_seq):
    patient_with_repeat_seq_txt = open(config.train_repeat_seq_txt, mode='w')
    keywords = ['ANY', 'TRA', 'ADC', 'BVAL', 'DWI']
    for index in range(len(repeat_seq)):
        patient_with_repeat_seq_txt.write(keywords[index] + ":" + '\n')

        for patient in repeat_seq[index]:
            patient_with_repeat_seq_txt.write(patient + '\n')

        patient_with_repeat_seq_txt.write('\n')


if __name__ == "__main__":

    standard_seq = get_standard_seq()
    patient_with_repeat_seq = get_patient_with_repeat_seq(standard_seq)
    print_repeat_seq_2_txt(patient_with_repeat_seq)

