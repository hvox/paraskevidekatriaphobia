game.zip: static/*
	rm -rf build; mkdir build
	scripts/minify static/script.js > build/script.js
	cp static/*.bin static/styles.css static/index.html build/
	( cd build/ && zip game.zip * )
	mv build/game.zip game.zip
	wc -c game.zip
