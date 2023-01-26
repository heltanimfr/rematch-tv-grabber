import re, sys, tempfile, os
from requests import get  # to make GET request

def download(url, local_filename):
    # open in binary mode
    print(f"Downloading {url} -> {local_filename}")
    with open(local_filename, "wb") as file:
        response = get(url)        
        file.write(response.content)
        file.close()
    
def get_all_master_playlists(temp_dir:str, root_playlist_url:str) -> list:
    sub_master_playlist_files_list = []    
    filename = os.path.normpath(
                            os.path.join(temp_dir, os.path.basename("index.dict")))
    # download master file
    download( root_playlist_url, filename )
    with open(filename, 'r') as f:
        urls = re.findall(r'[(https://)]*?\w*[(/{1})]?[#-\./\w]*[(/{1,})]?m3u8', f.read())
        # download all sub_master playlist
        for url in urls:                
            media_playlist = os.path.normpath(
                            os.path.join(temp_dir, os.path.basename(url)))
            media_dir_url = os.path.dirname( url )
            download( url, media_playlist )
            with open(media_playlist, 'r') as g:
                """ """
                data = g.read().split()
                for pl_url in data:
                    if not pl_url.startswith('#'):
                        # get first quality (720p) here
                        sub_master_playlist_files_list.append( f"{media_dir_url}/{pl_url}" )
                        break
                g.close()            
        f.close()
    return sub_master_playlist_files_list

def get_media_files(temp_dir:str, list_of_master_playlist) -> list:
    # reorder by playlist ?
    list_of_master_playlist.sort()
    media_files_list = []
    for sub_master_playlist_url in list_of_master_playlist:
        filename = os.path.normpath(
                            os.path.join(temp_dir, os.path.basename(sub_master_playlist_url)))
        # download master file
        root_dir = '/'.join( sub_master_playlist_url.split('/')[:-1])
        download( sub_master_playlist_url, filename)
        pl_file = open( filename)            
        media_files_list.extend( [ f"{root_dir}/{media_url}" for media_url in pl_file.read().split() if media_url.endswith('ts') or media_url.endswith('mp4') ] )
        pl_file.close()
    return media_files_list
    
def download_all_media_files( output_dir:str, list_media_files ):    
    for media in list_media_files:
        media_filename_wo_dir = ''.join( media.split('/')[-1])
        local_filename = os.path.normpath( 
                                            os.path.join( output_dir, media_filename_wo_dir) )
        download( media, local_filename)

def _main(entry_url:str, output_dir:str):
    with tempfile.TemporaryDirectory() as temp_dir:
        list_master_playlist = get_all_master_playlists(temp_dir, entry_url)
        list_media_files     = get_media_files( temp_dir, list_master_playlist )
        download_all_media_files(output_dir, list_media_files)        
                
if __name__ == "__main__":    
    root_playlist_url=f'''https://cf.api.rematch.fr/videos?matchID=ceqlbc2bib6s70ask0lg''' # u13 janze - cobse
    root_playlist_url=f'''https://cf.api.rematch.fr/videos?matchID=ceql5mb9vues708mkm00''' # loisirs bain - cobse
    root_playlist_url=f'''https://cf.api.rematch.fr/videos?matchID=cev7mbi8ajoc70ehljfg''' # seniors cobse - 
    output_dir="/home/TMP/Rematch/"
    # for i in *.ts; do cat $i>>all.ts;done
    # ffmpeg -i all.ts -vcodec copy -acodec copy cobseU13.mp4
    sys.exit( _main( root_playlist_url, output_dir ) )
