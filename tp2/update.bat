rm tp2.zip
git add .
git commit -m "TP2 Update"
git push
7z a -tzip "tp2.zip" "proposal.pdf" "storyboard.jpg" "src/*.py"  "src/icon.png" "styles/images" "styles/*/style.jpg" "styles/*/preview.jpg" "styles/*/cfg.txt" "src/dump/" "README.txt" 
