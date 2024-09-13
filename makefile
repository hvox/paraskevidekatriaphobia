game.zip: static/font.bin static/index.html static/models.bin static/quads.fs.glsl static/quads.vs.glsl static/script.js static/shader.fs.glsl static/shader.vs.glsl static/styles.css
	rm -rf build; mkdir build
	scripts/minify static/script.js > build/script.js
	cp static/*.bin static/styles.css static/index.html build/
	( cd build/ && zip game.zip * )
	mv build/game.zip game.zip
	wc -c game.zip

static/font.bin: scripts/font.py
	python3 scripts/font.py

static/models.bin: models.blend scripts/export.py
	blender models.blend -b --python scripts/export.py
	mv models.bin static/models.bin
