# Spotify API

* Create a [Spotify Application](https://developer.spotify.com/dashboard/applications)
* Take note of:
    * `Client ID`
    * `Client Secret`
* Click on **Edit Settings**
* In **Redirect URIs**:
    * Add `http://localhost/callback/`

# Refresh Token

* Navigate to the following URL:

```
https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&scope=user-read-currently-playing,user-read-recently-played&redirect_uri=http://localhost/callback/
```

* After logging in, save the {CODE} portion of: `http://localhost/callback/?code={CODE}`

* Create a string combining `{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}` (e.g. `5n7o4v5a3t7o5r2e3m1:5a8n7d3r4e2w5n8o2v3a7c5`) and **encode** into [Base64](https://base64.io/).

* Then run a [curl command](https://httpie.org/run) in the form of:
```sh
curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -H "Authorization: Basic {BASE64}" -d "grant_type=authorization_code&redirect_uri=http://localhost/callback/&code={CODE}" https://accounts.spotify.com/api/token
```

* Save the Refresh token

# Deployment

## Deploy to Vercel

* Register on [Vercel](https://vercel.com/)

* Fork this repo, then create a vercel project linked to it

* Add Environment Variables:
    * `https://vercel.com/<YourName>/<ProjectName>/settings/environment-variables`
        * `SPOTIFY_REFRESH_TOKEN`
        * `SPOTIFY_CLIENT_ID`
        * `SPOTIFY_SECRET_ID`

* Deploy!

# Readme

You can now use the following in your readme:

```[![Spotify](https://USER_NAME.vercel.app/api/spotify)](https://open.spotify.com/user/USER_NAME)```

# Customization

## Hide the EQ bar

Remove the `#` in front of `contentBar` in [line 81](https://github.com/novatorem/novatorem/blob/98ba4a8489ad86f5f73e95088e620e8859d28e71/api/spotify.py#L81) of current master, then the EQ bar will be hidden when you're in not currently playing anything.

## Status String

Have a string saying either "Vibing to:" or "Last seen playing:".

* Change [`height` to `height + 40`](https://github.com/novatorem/novatorem/blob/5194a689253ee4c89a9d365260d6050923d93dd5/api/templates/spotify.html.j2#L1-L2) (or whatever `margin-top` is set to)
* Uncomment [**.main**'s `margin-top`](https://github.com/novatorem/novatorem/blob/5194a689253ee4c89a9d365260d6050923d93dd5/api/templates/spotify.html.j2#L10)
* Uncomment [currentStatus](https://github.com/novatorem/novatorem/blob/5194a689253ee4c89a9d365260d6050923d93dd5/api/templates/spotify.html.j2#L93)

## Theme

Pick a preset bundle of colors via the `theme` param (default: `dark`):

- `?theme=dark`
- `?theme=light`

Individual color params override the preset, so `?theme=light&background_color=000000` gives the light preset with a black background.

## Color

You can customize the appearance of your `Card` however you wish with URL params. All take a hex color _(no `#`)_.

### Card:

- `background_color` - Card background
- `border_color` - Card border

### Text:

- `text_primary` - Song title
- `text_secondary` - Artist name
- `status_color` - "Now playing" / "Recently played" label

### EQ Bars:

- `bar_low` - Gradient end-stops (the muted edges of each bar)
- `bar_high` - Gradient midpoint (the bright pulse)

### Animation:

- `speed` - EQ bar speed. Higher = faster. Default: `1.0` (min `0.4`, max `2.5`).
- `grad` - Gradient sweep speed. Higher = faster. Default: `1.0`. Use `0` to freeze.

Example:
&nbsp; <br> `https://YOUR_DOMAIN.vercel.app/api/spotify?theme=light&speed=0.7&grad=0.1`

## Spotify Logo

You can add the spotify logo by removing the commented out code, seen below:
```html
<a href="{{songURI}}" class="spotify-logo">
    <svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>Spotify</title><path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/></svg>
</a>
```

## Requests

Customization requests can be submitted as an issue, like https://github.com/novatorem/novatorem/issues/2

If you want to share your own customization options, open a PR if it's done or open an issue if you want it implemented by someone else.

# Debugging
If you have issues setting up, try following this [guide](https://youtu.be/n6d4KHSKqGk?t=615).

Followed the guide and still having problems?
Try checking out the functions tab in vercel, linked as:
```https://vercel.com/{name}/spotify/{build}/functions```

<details><summary>Which looks like-</summary>

![image](https://user-images.githubusercontent.com/16753077/91338931-b0326680-e7a3-11ea-8178-5499e0e73250.png)

</details><br>

You will see a log there, and most issues can be resolved by ensuring you have the correct variables from setup.

## Source
This file is copied from [novatorem](https://github.com/novatorem/novatorem).
