# VISUALISATION SERVER

This nodejs based server serves the web-frontend of the project.
It uses the EJS templating engine, all other script functionalities are only on the javascript side.
Here simple Vanilla Javascript, Bootstrap, Jquery and D3.js + Geo Extension is used.

This application can be started using `node server.js` or by using the Dockerfile `docker run -it -p 3016:3016 .`.
All generated datasets from the jupyther notebooks are stored in the `./public/visualisation_files/generated`.
This folder contains a 1:1 copy of the following directory:  `../generated`.

This webserver only require this files to run, no further internet connection needed.

Please see the `./views/index.ejs` for the full frontend html file, including documented js code.