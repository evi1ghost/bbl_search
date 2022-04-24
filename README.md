# bbl_search
App to search the information about districts and plots in NYC by Borough/Block/Lot (BBL) numbers.
## Installation:
### Install Docker and Docker Compose:
Use instruction for your OS:
- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Set login attributes for MySQL:
If you want to change default login attributes rename [.env.example](.env.example) to .env and set desired values.
### Run initializing scripts:
```sh
sudo ./init_mysql.sh
./init_app.sh
```
### Activate virtual environment:
`source venv/bin/activate`
### Run the app:
`bbl_search --help`
## Usage:
| Command | Description |
| ---------------- | ---------------- |
| `--help`         | Show help message with command list.                |
| `area-range`     | Show max and min areas of plots.                    |
| `bbl`            | Search plot by bbl.                                 |
| `delete`         | Delete plots with areas within interval.            |
| `districts-info` | Show info about districts having at least one plot. |
| `flush`          | Restore deleted plots.                              |
