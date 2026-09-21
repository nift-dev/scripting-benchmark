import glob
print(len(glob.glob('benchmarks/sources/filesystem/traverse/small_tree/**/*.txt', recursive=True)))
