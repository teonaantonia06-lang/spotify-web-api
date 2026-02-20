Spotify Genre Explorer & Playlist Organizer
Overview

This project is a personal experiment to explore how Spotify categorizes music genres — especially rock and metal — by using Spotify’s public API to automatically organize tracks from a playlist into genre-based playlists.

The goal is not to create a perfect genre classification system, but to:
* Observe how fragmented Spotify’s genre labels are
* Understand how microgenres are applied to artists
* Learn how APIs work in practice

This project is intentionally exploratory and iterative.

Motivation
I’ve always found subgenres — especially in rock and metal — confusing and interesting at the same time. Spotify clearly has a very granular genre system, but this information is not easily visible in the UI.

By working directly with Spotify’s API, I want to:
* See which genre labels are actually used
* Understand how many genres are assigned per artist
* Observe overlap between genres
* Discover unexpected or niche genre groupings
* Learn through experimentation rather than theory

Part of this project is purely for fun, part of it is driven by curiosity about how classification systems behave at scale.

***Project Scope (Initial Version)***
Input:
A single Spotify playlist

Process:
* Fetch all tracks from the playlist
* Retrieve genre labels from each track’s primary artist
* Create one playlist per genre
* Add each track to every playlist that matches its artist’s genres

Output:
* A large set of genre-based playlists
* Significant overlap between playlists is expected and accepted
* No genre normalization or mapping is applied in the first iteration.

Assumptions & Expectations (Before Running)
* Artists will typically have multiple genre labels (roughly 2–5)
* Rock and metal artists will often include a root genre (rock or metal), plus several microgenres
* Genre fragmentation will be high, especially for metal
* Many playlists will end up very small
* The results will be imperfect, but informative

Known Limitations:
Genres are assigned per artist, not per track
=> Individual songs may not match the artist’s overall genre


No attempt is made to:
* Rank genre relevance
* Merge similar genres
* Filter out low-quality playlists automatically

These limitations are accepted as part of the experiment.


Manual Cleanup Strategy
After running the script:
* Playlists with very few tracks (e.g. <10 songs) can be deleted manually
* Interesting or unexpectedly cohesive playlists can be kept
* If fragmentation is excessive, genre mapping may be introduced in a later iteration
* Manual pruning is considered part of the learning process.

Learning Goals
This project is primarily about learning:
* How to work with real-world APIs
* How authentication and rate limiting work
* How messy real data is compared to theory
* How large systems classify and label information
* How to iterate on imperfect first solutions

Future Ideas (Optional)
* Genre normalization / mapping
* Grouping microgenres under umbrella genres
* Logging genre frequency statistics
* Visualizing genre fragmentation
* Comparing rock vs metal vs other genres
None of these are required for the initial version.

Final Notes
This project is an exploration, not a product.
Imperfection is expected.
Curiosity comes first.


Improvements
* Scripts for sorting into genre based playlists both all user tracks and a playlist ID 
* The dryrun.py script can be used to test the connection (it was used during implementation for testing as well)
* Implemented a system that can create a new to-sort playlist based on an already existing playlists with the already sorted songs 
(the to-sort playlist can then be used as input)
* Added utils scripts for a diversity of smaller actions that a user might need to do
(deleting the playlists created any of these scripts, finding all the songs without genres from a playlists,
printing all genres presented in a playlist, printing an artist's genres)