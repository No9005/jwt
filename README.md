# jsonWebToken
This package wraps the 'authlib' jwt class. <br>
For indepth information about the package you should check out the developers [homepage](https://docs.authlib.org/en/latest/).

## Content
1. [general](#general)
2. [installation](#installation)
3. [usage](#usage)
    - [`with_rsa`](#usage-with_rsa)
    - [`with_secret`](#usage-with_secret)
4. [debbuging](#debugging)
5. [reference](#reference)

<br>

# <a name="general"></a> 1. general

There are basically two shortcuts to use:
- **with_rsa**: Uses a **private** and **public** rsa.pem to build the signature
- **with_secret**: Uses a **secret (str)** to build the signature

You can pass an expiration time for both cases, after which the token expires automatically.

<br>

# <a name="installation"></a> 2. installation
You can install the package by either downloading the source code manually and running `pip install` or by installing from the github repo.

## I. by downloading the source
You can click on the download button or run in your terminal:

<br>

```terminal
$ git clone https://github.com/No9005/jwt
```

<br>

> _Note:_ <br>
> _You have to install **git** first (if not already installed) to run the above code._

<br>

After downloading (either way is legit) the code, you can install it by using:

<br>

```terminal
$ git install 'path/to/the/folder'
```

<br>

where `path/to/the/folder` is your path to the download directory.

## II. by pip installing
You do not have to download the source code first. Pip is able to install directly from the jwt repo by using: 

<br>

```terminal
$ pip install git+https://github.com/No9005/jwt
```

<br>

# <a name="usage"></a> 3. Usage
## <a name="usage-with_rsa"></a>  I. `with_rsa`
This group of functions create and decode JWT tokens by utilizing the 'RS256' algorithmn and a **public** and **private** rsa key.

<br>

> _Note:_<br>
> _For a guide to generate public/private rsa keys (linux) you can check out this [ressource](https://developers.yubico.com/PIV/Guides/Generating_keys_using_OpenSSL.html)._

<br>

Import the method with:

<br>

```python
from jsonWebToken import with_rsa
```

<br>

Afterwards you can use the `create()` and `decode()` functions to create and decode the tokens like this:

<br>

```python
# create token
token = with_rsa.create(
    payload = {
        'your-claim':'the-value',
        'next-claim':'next-value',
        ...
    },
    private_key = 'private-rsa-as-string',
    expiration = 600
)
```

<br>

whereas:
- `payload`: **dict** containing your claims.
- `private_key`: **str** of your loaded **private-key.pem** file.
- `expiration`:  **int** or **None**. Indicates the expiration time in seconds.
    - If **None** (or `expiration = 0`) the token does not expire.
    - Default is 600s (aka 10min.)

<br>

> _Note:_ <br>
> _A **claim** is nothing else than a **key:value** pair of a dictionary. It's just called **claim** in the context of JWT-tokens._ <br>
> <br>
> _Keep in mind though, that you have to use **key:value** pairs which are legtime in python and also are jsonifyable (meaning you can't pass a pandas DataFrame for example)!_

<br>

After running the function you receive a JWT-Token which is signed by your private key.

<br>

```python
# print token
print(token)

>> b'jWasjelc-Ec.....'
```

<br>

The decoding of your generated token is done like this:

<br>

```python
# decode token, returns a dict containing 'success', 'error' and 'payload'
content = with_rsa.decode(
    token = token,
    public_key = 'public-rsa-as-string'
)

>> {'success':True, 'error':"", 'payload':{'your-claim':'the-value', ...}}
```

<br>

You will receive a python dictionary with the following keys:
- `success`: **bool**. Indicates if the token decoding was successfull
- `error`: **str**. Contains the error message (if the process did not succeed). Reasons:
    - Token expired: The token lifetime passed the `expiration` limit.
    - Token has bad signature: Someone tampered with the token content, thus the signature
    - Token is not in the package format: You passed a token that is not in the correct format to work with this package (aka you used a token generated by another source).
- `payload`: **dict**. If the decoding was successfull, you will find your token payload as python dictionary here. 
    - **CAUTION**: You will not receive a payload if the decoding process was not successfull (because you can't trust the info anyway.)

<br>

## <a name="usage-with_secret"></a>  I. with_secret
The encoding during the creation process is done by using the 'HS256' algorithmn. Thus you only need one secret phrase to encode and decode the token.

<br>

To use the functions you have to import the `with_secret` module:

<br>

```python
from jsonWebToken import with_secret
```

<br>

You can create a token with the `create()` function:

<br>

```python
# create a token
token = with_secret.create(
    payload = {
        'claim':value,
        'claim2':value,
        ....
    },
    secret = 'your-secret-phrase',
    expiration = 600
)

# ... and you receive something like this:
print(token)

>> b'aeJedCjEC.....'
```

<br>

whereas:
- `payload`: **dict** containing your claims.
- `secret`: **str**. Your secret phrase to validate the signature.
- `expiration`:  **int** or **None**. Indicates the expiration time in seconds.
    - If **None** (or `expiration = 0`) the token does not expire.
    - Default is 600s (aka 10min.)

<br>

The decoding of your generated token is done like this:

<br>

```python
# decode token, returns a dict containing 'success', 'error' and 'payload'
content = with_rsa.decode(
    token = token,
    secret = 'secret-phrase-used-during-creation'
)

>> {'success':True, 'error':"", 'payload':{'claim':value, ...}}
```

<br>

You will receive a python dictionary with the following keys:
- `success`: **bool**. Indicates if the token decoding was successfull
- `error`: **str**. Contains the error message (if the process did not succeed). Reasons:
    - Token expired: The token lifetime passed the `expiration` limit.
    - Token has bad signature: Someone tampered with the token content, thus the signature
    - Token is not in the package format: You passed a token that is not in the correct format to work with this package (aka you used a token generated by another source).
- `payload`: **dict**. If the decoding was successfull, you will find your token payload as python dictionary here.
    - **CAUTION**: You will not receive a payload if the decoding process was not successfull (because you can't trust the info anyway.)

<br>

## <a name="debugging"></a> 4. debugging
If you want to check the correctness of the token, you can use the following [site](https://jwt.io/).<br>
Keep in mind that you have to select the correct signing algorithmn. These are:
- `with_rsa`: RS256
- `with_secret`: HS256

<br>

> _Note:_ <br>
> _This package creates signed but not encrypted tokens! You can see this by using the token decryptor from [jwt.io](https://jwt.io/)._ <br>
> _Thus, you should **never ever** transmit user sensitive data within the token payload!!!!_

<br>

## <a name="references"></a> 5. references
[1] Python authlib: https://docs.authlib.org/en/latest/ <br>
[2] JWT intro: https://jwt.io/introduction <br>
[3] Generating public/private rsa keys: https://developers.yubico.com/PIV/Guides/Generating_keys_using_OpenSSL.html

<br>

