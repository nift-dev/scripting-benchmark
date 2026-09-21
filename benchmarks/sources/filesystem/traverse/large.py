import glob
print(len(glob.glob('benchmarks/sources/filesystem/traverse/large_tree/**/*.txt', recursive=True)))
