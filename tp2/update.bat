rm tp2.zip
git add .
git commit -m "TP2 Update"
git push
7z a -tzip "tp2.zip" "proposal.pdf" "storyboard.jpg" "src/*.py"  "src/icon.png" "styles/*/style.jpg" "style/*/preview.jpg" "styles/*/cfg.txt" "src/dump/tex1_48x24_f2707ea31b3c1aa8_14.dds" 
