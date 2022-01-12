for png in `find $1 -name "*.png"`;
do
	pngquant --quality=100 --strip -f --nofs --skip-if-larger --output "$png" "$png"
done;
echo "Done."
