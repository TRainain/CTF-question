# Hints

There's no RCE, R/W. Only XSS.

## Run program

To run the program with all development features, you can use the following commands:

```shell
pnpm install
pnpm build
pnpm test # or `pnpm run start:dev`
```

It's recommended to visit the program on localhost or over HTTPS, for some features only work on them due to browser security policies.

## Fast reading

The following hints may help you locate the important codes more quickly:

- Line in `app.main.mjs:238`
- Function in `src/middleware.mjs:102`
- Function in `src/middleware.mjs:112`
- Line in `app.assets.mjs:32`

## Project structure

Followings are the structure of this project:

- `app.main.mjs`: Main application
- `app.assets.mjs`: Static assets (local visit only)
- `src/`: Back-end source code
- `public-src/`: Front-end source code
- `views/`: Front-end HTML templates
- `public/`: Front-end build output
- `assets/`: Static assets (local visit only)
