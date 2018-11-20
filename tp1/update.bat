rm tp1.zip
git add .
git commit -m "Update"
git push
7z a -tzip "tp1.zip" "proposal.pdf" "storyboard.png" "src/" "styles/" 
