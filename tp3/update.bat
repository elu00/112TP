rm tp3.zip
git add .
git commit -m "TP3 Update"
git push
7z a -tzip "tp3.zip" "proposal.pdf" "storyboard.jpg" "src/*.py"  "src/icon.png" "styles/*/style.jpg" "styles/*/preview.jpg" "styles/*/cfg.txt" "src/dump/" "README.txt" 
