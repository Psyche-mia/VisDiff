from huggingface_hub import try_to_load_from_cache, _CACHED_NO_EXIST
from huggingface_hub import scan_cache_dir

filepath = try_to_load_from_cache(cache_dir="/mnt/.cache/huggingface/hub", 
                                  repo_id="bert-base-uncased", 
                                  filename="config.json")

if isinstance(filepath, str):
    # file exists and is cached
    print("file exists and is cached")
elif filepath is _CACHED_NO_EXIST:
    # non-existence of file is cached
    print("non-existence of file is cached")
else:
    # file is not cached
    print("file is not cached")
    
