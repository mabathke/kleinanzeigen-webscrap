# Immobilien Kleinanzeigen Web Scraper

This project is a web scraper designed to extract real estate listings from the Kleinanzeigen website for a specific location. The scraper retrieves and prints the title, price, location, and date of each listing. I just started this project and I am still working on it. I plan to add more features to it in the future. The goal is to create and application (containerized) that will allow users to search for real estate listings in a specific location and store the data in a database. The scrappe should than be able to get a history of the listings and compare the prices to see if the price has increased or decreased. 
## Current TODOS
- [x] Create a web scraper that extracts the title, price, location, and date of each listing
- [ ] Create a database to store the data
- [ ] Optimize the scraper
  - [ ] Improve pagination -> Currently only 10 pages are scraped. Handle if the last span is ... and get the last page number
  - [ ] Need some logic to get an ID for each listing and then get a timestamp for each listing -> This will allow us to get the history of the listings


## What 