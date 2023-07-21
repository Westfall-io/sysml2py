# Changelog

<!--next-version-placeholder-->

## v0.4.0 (2023-07-21)

### :sparkles:

* :sparkles: Added a new base model class to replace collapse function. Model will create packages and other custom classes for use. Additionally, packages can be created from grammar. ([`3dc5fca`](https://github.com/Westfall-io/sysml2py/commit/3dc5fcad2e892b0e14c1c9f74cbea868df6844a5))
* :sparkles: Added port with ability to create subfeatures with directionality. ([`94c0a19`](https://github.com/Westfall-io/sysml2py/commit/94c0a19b08203a3db953858bf968de5c2f2084bc))
* :sparkles: New package class. ([`3766690`](https://github.com/Westfall-io/sysml2py/commit/3766690bd848de0475eb047af1870da358dd51ab))

### :bug:

* :bug: Fix for definition naming. ([`ff62dc1`](https://github.com/Westfall-io/sysml2py/commit/ff62dc10131d8c53fd4361f7100403dc1c4424f6))
* :bug: Reverting change to author. ([`ae5d19e`](https://github.com/Westfall-io/sysml2py/commit/ae5d19e5581b3493e985bd01bb356b1dcd3d1618))
* :bug: Added test and definition file that was causing the error. ([`b7787d4`](https://github.com/Westfall-io/sysml2py/commit/b7787d4ccba53e421e3f877a46eca331698e2950))
* :bug: Fixed an issue where something defined within a package could not be typed by another definition ([`ee257eb`](https://github.com/Westfall-io/sysml2py/commit/ee257eba9cdaec2a8ac52f65cf702881879aa445))

### :heavy_plus_sign:

* :heavy_plus_sign: Using poetry package management, added dependencies. ([`5c625dd`](https://github.com/Westfall-io/sysml2py/commit/5c625dd6e51a6090a699aab229c335d8946d7bd5))
* :heavy_plus_sign: Adding pytest-html to test workflow. ([`4f2cedc`](https://github.com/Westfall-io/sysml2py/commit/4f2cedc50162ac2013b5dc60481a7bc646debad3))

### Other

* Merge pull request #39 from Westfall-io/dev0.4.x ([`5add8f1`](https://github.com/Westfall-io/sysml2py/commit/5add8f10ca84601cedd26a55653b3c825f213f16))
* Merge pull request #38 from Westfall-io/31-pypi-package-doesnt-load-dependencies ([`a22b756`](https://github.com/Westfall-io/sysml2py/commit/a22b7569162f30ca19d20e46b0963ab640b8f869))
* Merge pull request #37 from Westfall-io/dev0.4.x ([`cd8982d`](https://github.com/Westfall-io/sysml2py/commit/cd8982dd6eef8076b17c54273039a27846b3bb3e))
* Merge pull request #36 from Westfall-io/31-pypi-package-doesnt-load-dependencies ([`39e88e3`](https://github.com/Westfall-io/sysml2py/commit/39e88e3ba6f1bd55f6d4f408fe9a18799a38d4da))
* Merge pull request #35 from Westfall-io/dev0.4.x ([`5a89864`](https://github.com/Westfall-io/sysml2py/commit/5a8986468bb7ff7f75eb8b5b8068f5e4d9a92bce))
* Merge pull request #34 from Westfall-io/31-pypi-package-doesnt-load-dependencies ([`ef4d860`](https://github.com/Westfall-io/sysml2py/commit/ef4d8603d4107bbec1a74f732eb543190b8a418d))
* :memo: Updates to project info to assist sphinx build. ([`939d2ff`](https://github.com/Westfall-io/sysml2py/commit/939d2ff4867ccc792b78c8a1229ef937653093ec))
* Merge pull request #33 from Westfall-io/dev0.4.x ([`f23a4c2`](https://github.com/Westfall-io/sysml2py/commit/f23a4c28bbcbcf58a012ae59c340077de873ba3e))
* Merge pull request #32 from Westfall-io/31-pypi-package-doesnt-load-dependencies ([`e39c8f4`](https://github.com/Westfall-io/sysml2py/commit/e39c8f4bd1c8425ae9c501ce22e7c0ad5d77e1e2))
* Merge pull request #30 from Westfall-io/26-package-class-cannot-load-from-grammar ([`b9744c7`](https://github.com/Westfall-io/sysml2py/commit/b9744c78f44e5025f57b339f69b8a97d3b9345cd))
* :white_check_mark: Adding child as optional to get def functions. ([`da90c49`](https://github.com/Westfall-io/sysml2py/commit/da90c49e3b6d80258ea6bdc2391031ead534833f))
* :white_check_mark: Correcting tests ([`fba8dce`](https://github.com/Westfall-io/sysml2py/commit/fba8dcef847f4d5c39ad97c72b9cb711236df335))
* :robot: Format code with black ([`95a70fe`](https://github.com/Westfall-io/sysml2py/commit/95a70feca54d696616c9a263e77d8d8ec75496e4))
* :poop: Fix merge conflicts. ([`14e38c5`](https://github.com/Westfall-io/sysml2py/commit/14e38c51756012a93ebeada0b9ad6a289d4c373a))
* :robot: Format code with black ([`0ea0415`](https://github.com/Westfall-io/sysml2py/commit/0ea04154d5e40630b8b9544616f0fc5be8de69e8))
* Merge branch 'dev0.4.x' of github.com:Westfall-io/sysml2py into 26-package-class-cannot-load-from-grammar ([`39de5e6`](https://github.com/Westfall-io/sysml2py/commit/39de5e639cee6f4155a1a10804eb8123980f5d9b))
* Merge pull request #29 from Westfall-io/25-create-custom-port-class ([`11bfed8`](https://github.com/Westfall-io/sysml2py/commit/11bfed83a809af7f4f533eb80140038e026148ac))
* 💩 Initial commit swapping to custom class focus rather than grammar. ([`1da3ea8`](https://github.com/Westfall-io/sysml2py/commit/1da3ea85363454da202db6ec6faef97dbc773781))
* Merge branch '25-create-custom-port-class' of github.com:Westfall-io/sysml2py into 25-create-custom-port-class ([`4b00cb0`](https://github.com/Westfall-io/sysml2py/commit/4b00cb0a61353a05cdb87b78bd295f4f8631bd2c))
* :robot: Format code with black ([`b87f1bf`](https://github.com/Westfall-io/sysml2py/commit/b87f1bf92aa79b5b8c7f2f3224338e38dc63b470))
* :construction_worker: Adding src to path for pytest in pyproject.toml ([`510d672`](https://github.com/Westfall-io/sysml2py/commit/510d672b98c747c7ad573aa1d7fbf28d2252b4a1))
* :construction_worker: Corrected test directory again. ([`92d5dc2`](https://github.com/Westfall-io/sysml2py/commit/92d5dc2c1bf1f416d6e248ddbf4bb45727a3e5fe))
* :construction_worker: Corrected test directory. ([`2bfc6df`](https://github.com/Westfall-io/sysml2py/commit/2bfc6dfc1f6767a4caddd0e69fbc459fc5a0ed4a))
* :green_heart: Adding coveralls to all branches. ([`425024d`](https://github.com/Westfall-io/sysml2py/commit/425024d1b7ebf80010c2f8a7e7d866b32ba4e5d8))
* Merge branch 'dev0.4.x' of github.com:Westfall-io/sysml2py into dev0.4.x ([`4290383`](https://github.com/Westfall-io/sysml2py/commit/429038303811a9cde716c0b0f82f9bb325cf1405))
* :construction_worker: Adding html to artifacts. ([`4b74045`](https://github.com/Westfall-io/sysml2py/commit/4b74045fc81d32fe33629dc215d1126145f572c3))
* :robot: Format code with black ([`2baf295`](https://github.com/Westfall-io/sysml2py/commit/2baf295cc7863f7e6654d51108b77e3cbc3c6486))
* :green_heart: Adding conftest.py ([`dbd32b9`](https://github.com/Westfall-io/sysml2py/commit/dbd32b967febd7396de40ff7e73a9b75182e7507))
* :green_heart: Adding path to init to correct test workflow. ([`d29bfb6`](https://github.com/Westfall-io/sysml2py/commit/d29bfb6692d950bf384182dda96ebb017c8231af))
* Merge pull request #28 from Westfall-io/27-add-trello-board-to-readmemd ([`c67ea22`](https://github.com/Westfall-io/sysml2py/commit/c67ea220243fa0bdeadeb5dde4dc83aed0a4186b))
* :memo: Fixing spacing. ([`25e78d0`](https://github.com/Westfall-io/sysml2py/commit/25e78d01066b96146be587988e1735367747f52c))
* :memo: Adding more badges. ([`76899b1`](https://github.com/Westfall-io/sysml2py/commit/76899b192545087066493c7a65c388266c09d01c))
* :memo: Added trello to Readme ([`26e304c`](https://github.com/Westfall-io/sysml2py/commit/26e304c10ea7599259d75f43992996887161183a))
* Merge pull request #24 from Westfall-io/23-create-a-custom-package-class ([`213b599`](https://github.com/Westfall-io/sysml2py/commit/213b599e350ac7c77d8967f50b2fb6c71547106c))
* :robot: Format code with black ([`24e051d`](https://github.com/Westfall-io/sysml2py/commit/24e051d8339c50c21ce173c364aa93fb96c0b633))
* Merge branch '23-create-a-custom-package-class' of github.com:Westfall-io/sysml2py into 23-create-a-custom-package-class ([`f752ac3`](https://github.com/Westfall-io/sysml2py/commit/f752ac3a16693a2c9547f3807bb669066bb7cf57))
* :white_check_mark: Package tests added. ([`803192b`](https://github.com/Westfall-io/sysml2py/commit/803192b75749facc0d19cae596038663b3708714))
* :robot: Format code with black ([`4dcc4c9`](https://github.com/Westfall-io/sysml2py/commit/4dcc4c9cc5ba70752934430f477f64a41f09ef16))
* :robot: Format code with black ([`1651fdb`](https://github.com/Westfall-io/sysml2py/commit/1651fdbb80771a87afe94082df4a177adc37bc54))

## v0.3.1 (2023-07-11)

### Other

* Merge pull request #22 from Westfall-io/dev0.3.1 ([`8dc6722`](https://github.com/Westfall-io/sysml2py/commit/8dc6722aa809565a86d5e9bf7c506b60864fb2fd))
* Merge branch 'dev0.3.1' of github.com:Westfall-io/sysml2py into dev0.3.1 ([`151be3f`](https://github.com/Westfall-io/sysml2py/commit/151be3fd591918aa2bfee475395218e33b712e47))
* Merge branch 'main' of github.com:Westfall-io/sysml2py into dev0.3.1 ([`76dc161`](https://github.com/Westfall-io/sysml2py/commit/76dc1616092fd20c5f1d5f27cf6d991f590b162b))
* :robot: Format code with black ([`0b70bbc`](https://github.com/Westfall-io/sysml2py/commit/0b70bbc00d82781d894fbf088d5e52831088c7ae))
* :memo: Documentation changes. ([`edfd629`](https://github.com/Westfall-io/sysml2py/commit/edfd629ec5ef6611d2b9643706cee6b1bf40ea47))

## v0.3.0 (2023-07-11)

### :sparkles:

* :sparkles: Added some rollup classes the abstract underlying grammar. They have functions to manipulate the grammar. ([`b1e01a4`](https://github.com/Westfall-io/sysml2py/commit/b1e01a465200e79f96a30da4f2ce5b861850ddd5))

### :arrow_up:

* :arrow_up: Merge from main and add astropy to main dependencies to handle units. ([`98f260b`](https://github.com/Westfall-io/sysml2py/commit/98f260b888f54f9f6911b043387cd0fbc4d81c88))

### Other

* Merge pull request #21 from Westfall-io/dev0.3.x ([`f83804e`](https://github.com/Westfall-io/sysml2py/commit/f83804e94d207807df160152ce1b55a0c91d7c9b))
* Merge pull request #20 from Westfall-io/19-provide-user-interactable-item-class ([`4d3dd0a`](https://github.com/Westfall-io/sysml2py/commit/4d3dd0a34b73c1db5a3c57bd2cc85f8d8055acb6))
* :robot: Format code with black ([`3cc027b`](https://github.com/Westfall-io/sysml2py/commit/3cc027bbb04e7ddcbc3422f3b11b4809913f985b))
* :poop: Fixing git conflict. ([`f44c394`](https://github.com/Westfall-io/sysml2py/commit/f44c394e15f78034fe83f3086d6b0cca58658052))
* :memo: Updates to readme, also added a loadfromgrammar function to Usage. ([`e999436`](https://github.com/Westfall-io/sysml2py/commit/e999436193ccee31dfadaf5a193705cf61e99496))
* :robot: Format code with black ([`f85c2a5`](https://github.com/Westfall-io/sysml2py/commit/f85c2a51f49954e032322d4603bb431e53392c65))
* 🚧 Merge from code black mods. ([`cde58c1`](https://github.com/Westfall-io/sysml2py/commit/cde58c1cef4149e79cd4e40ea39016f954da6354))
* Merge branch 'main' of github.com:Westfall-io/sysml2py into 19-provide-user-interactable-item-class ([`157d5f7`](https://github.com/Westfall-io/sysml2py/commit/157d5f73e00c58a0f7ddee8676585b741772e585))
* :robot: Format code with black ([`90398e1`](https://github.com/Westfall-io/sysml2py/commit/90398e15bfcbc54d20011c35a9f9384da91fd134))

## v0.2.10 (2023-06-21)

### Other

* Merge pull request #18 from Westfall-io/dev0.2.10 ([`b80720a`](https://github.com/Westfall-io/sysml2py/commit/b80720a95ed6e92bc221f1942cb511550d2f9139))

## v0.2.9 (2023-06-21)

### Other

* Merge pull request #17 from Westfall-io/dev0.2.9 ([`272d939`](https://github.com/Westfall-io/sysml2py/commit/272d939e3856a00550c9a4d17fe0c5a029f8466c))

## v0.2.8 (2023-06-21)

### Other

* Merge pull request #16 from Westfall-io/dev0.2.8 ([`c8d6be2`](https://github.com/Westfall-io/sysml2py/commit/c8d6be23cb840f9f009de22651656274ce612f38))

## v0.2.7 (2023-06-21)

### Other

* Merge pull request #15 from Westfall-io/dev0.2.7 ([`39e5f56`](https://github.com/Westfall-io/sysml2py/commit/39e5f56c291d45a163ee0e9739c4ed09b7894675))

## v0.2.6 (2023-06-21)

### Other

* Merge pull request #14 from Westfall-io/dev0.2.6 ([`6fd28b9`](https://github.com/Westfall-io/sysml2py/commit/6fd28b985cd561b64a7ea9746d8a7237f46f8662))

## v0.2.5 (2023-06-21)

### Other

* Merge pull request #13 from Westfall-io/dev0.2.4 ([`20c9db0`](https://github.com/Westfall-io/sysml2py/commit/20c9db087b56f7c39fec705a8b603886a14a0269))
* Merge branch 'main' of github.com:Westfall-io/sysml2py into dev0.2.4 ([`f5ec843`](https://github.com/Westfall-io/sysml2py/commit/f5ec8436dd51a41c76efa28cd564dac66d80126d))

## v0.2.3 (2023-06-21)

### Other

* Merge pull request #12 from Westfall-io/dev0.2.3 ([`be96ebb`](https://github.com/Westfall-io/sysml2py/commit/be96ebbb0bcfd5baffd9fad589ee4a280fa7c721))

## v0.2.2 (2023-06-21)

### Other

* Merge pull request #11 from Westfall-io/dev0.2.2 ([`f67e116`](https://github.com/Westfall-io/sysml2py/commit/f67e11669d3421b1754ca7b9a99db0aa25d8b0a7))

## v0.2.1 (2023-06-21)

### Other

* Merge pull request #10 from Westfall-io/dev0.2.1 ([`420a16d`](https://github.com/Westfall-io/sysml2py/commit/420a16d7c62dbc56426e539adfcd7828ea408855))
* :robot: Add coverage badge ([`199fa49`](https://github.com/Westfall-io/sysml2py/commit/199fa497bb06bc68ac897f2031d951ae55ce1f9e))

## v0.2.0 (2023-06-21)

### :sparkles:

* :sparkles: More tests. ([`41d1f5e`](https://github.com/Westfall-io/sysml2py/commit/41d1f5eb343c4afe02224fd6b9d68bed3f5cebaa))
* :sparkles: More tests and classes. ([`cd59e2e`](https://github.com/Westfall-io/sysml2py/commit/cd59e2e7b2ff2c2eeb599480293f09efabcd79d9))
* :sparkles: More badge for readme. ([`4be8d54`](https://github.com/Westfall-io/sysml2py/commit/4be8d54efb78fa6030c8c80702f13e9ce295c5da))

### :zap:

* :zap: Adding code coverage badge to readme. ([`c72fe86`](https://github.com/Westfall-io/sysml2py/commit/c72fe8699891d30a588abdafc27d3f030900a31a))

### :bug:

* :bug: Adding textx to requirements. ([`d3c1c76`](https://github.com/Westfall-io/sysml2py/commit/d3c1c767b39a68d67c0eea7802982de770c1bc48))
* :bug: Workflow fixes ([`9b883ea`](https://github.com/Westfall-io/sysml2py/commit/9b883eaef9932e80299dc94ede0646a2ceb1a405))

### :ambulance:

* :ambulance: Fixing merge errors from black ([`e101e70`](https://github.com/Westfall-io/sysml2py/commit/e101e70ea50ccd52cc5226c6860bcbe1b9411d3a))
* :ambulance: Fix for build script ([`4c6f238`](https://github.com/Westfall-io/sysml2py/commit/4c6f238afcf37c8620f082dfee19a8a4282a47e3))
