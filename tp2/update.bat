rm tp2.zip
git add .
git commit -m "Update"
git push
7z a -tzip "tp2.zip" "proposal.pdf" "storyboard.png" "src/" "styles/" 
