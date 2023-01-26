# rematch-tv-grabber
Download video content from rematch.tv based on the matchId set in parameter of the URL (network tab in firefox for instance)

![rematch](https://user-images.githubusercontent.com/30439433/214874563-f7cd1db7-ed59-4628-8203-8802a3cb39af.png)

Script downloads all ts files from the top quality : you may merge it later via ffmpeg for example
> for i in *.ts; do cat $i >> all_in_one.ts; done
> ffmpeg -i all_in_one.ts -vcodec copy -acodec copy file.mp4
