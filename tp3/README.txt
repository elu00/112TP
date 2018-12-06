ABOUT:
This project contains a copy of styledev.rt, a QT-based GUI that provides a useful and fluid framework for
performing style transfer in real time through modification of game assets and
textures.



USAGE:
To run the main application interface, run the following commands in your terminal of choice:
> cd /src/
> python app.py 

To run the benchmarking software, run the following commands in your terminal of choice:
> cd /src/
> python bench.py



DEPENDENCIES:
This project requries the following to be installed/present:
- Dolphin Emulator (included for Windows builds)
- A ISO file of Paper Mario: The Thousand Year Door
- PyQt
- PyQtGraph
- PyTorch
- Torch
- torchvision
- Python Imaging Library (PIL)

If anaconda is installed on the system, all of the necessary python libraries can be installed by running /src/install.bat

VIDEO LINK:


LIMITATIONS OF THE AUTOLAB COPY:
Just to ensure compatibility/minimizing the likelihood of crashes, a couple of things to note about this zip:
- All of the code written by me is contained within "/src/app.py" and "/src/fileManager.py"
- Most of the code in "/src/alg.py" has been modified from the link in the top of that file.
- Everything in "/dolphin/" is a (mostly) unmodified build of dolphin.
- I obviously don't own or claim any rights to the style images used or the game (TTYD)
- The style images and related assets have all been computed through using the program.
- Due to file size constraints, a significant number of files/dependencies have been removed, which significantly reduces the functionality of this demo. In particular,
	- The precomputed styles that are loaded into the application are incomplete. Although the style and preview images are still present, the actual computed assets are not present.
	- With no game file or modified assets pre-packaged, actually running modified versions of the game will not be possible.
- With that said, however, core functionality of the app and computing new styles should be entirely functional.
- To retrieve a full version of this build with the full precomputed assets and dolphin build, see https://github.com/elu00/112TP/tree/master/tp3
- That build still has an extra dependency of a game file, which can be loaded in through the interface.

