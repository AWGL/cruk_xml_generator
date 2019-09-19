import os

def locate_samples(path_to_project):
    samples_list = next(os.walk(path_to_project))[1]  # directories
    return samples_list