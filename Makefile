wacom-thingy.desktop: wacom-thingy template.desktop
	bash -c "echo Exec=${HOME}/.local/bin/wacom-thingy >> path"
	cat template.desktop path > wacom-thingy.desktop
	
install: wacom-thingy.desktop
	cp wacom-thingy ${HOME}/.local/bin/wacom-thingy
	cp wacom-thingy.desktop "${XDG_DATA_HOME}/applications/"

clean:
	rm wacom-thingy.desktop
	rm path
