from hyperliquid_lib.api import API
from signing import build_points_payload, build_tos_payload
import time
from eth_account import Account
import os
import csv
from random import randint

CSV_FILE_PATH = 'results.csv'

# PROXY = "http://username:pass@ip:port"
PROXY = None

def initialize_csv():
    """Initialize the CSV file with headers if it doesn't exist."""
    if not os.path.isfile(CSV_FILE_PATH):
        with open(CSV_FILE_PATH, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["address", "points", "accepted_genesis"])
            writer.writeheader()

def append_to_csv(acc_res):
    """Append a new entry to the CSV."""
    with open(CSV_FILE_PATH, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["address", "points", "accepted_genesis"])
        writer.writerow(acc_res)

def is_address_in_csv(address):
    """Check if an address is already in the CSV."""
    if not os.path.isfile(CSV_FILE_PATH):
        return False 
    
    with open(CSV_FILE_PATH, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['address'] == address:
                if row['accepted_genesis'] == 'True':
                    return True
                return False
    return False  

def calculate_total_points():
    """Calculate the total sum of points from the CSV."""
    if not os.path.isfile(CSV_FILE_PATH):
        return 0

    total_points = 0
    with open(CSV_FILE_PATH, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                total_points += int(row['points'])
            except ValueError:
                print(f"Invalid points value in row: {row}")
    return total_points

if __name__ == "__main__":
    initialize_csv() 
    api = API()

    file = open("pks.txt", "r")
    pks = [x.strip() for x in file.readlines()]
    file.close()

    total_points = calculate_total_points()
    print("Total points fetched so far:", total_points)

    for pk in pks:
        try:
            account = Account.from_key(pk)

            if is_address_in_csv(account.address):
                print("Account has been fetched already. Skipping", account.address)
                continue

            api.post("/info", {"type": "genesisCheck"}) #jic

            p = build_points_payload(account, int(time.time()))

            res = api.post("/info", p)

            acc_points = 0
            accepted_genesis = False
            if "success" in res and "userSummary" in res["success"] and res["success"]["userSummary"]:
                try:
                    dist_hist = res["success"]["userSummary"]["distributionHistory"]
                    for d in dist_hist:
                        if "points" in d:
                            acc_points += d["points"]
                    print("Points:", acc_points)
                except Exception as e:
                    print("Error fetching acc points", account.address, e)
            elif "alreadyAcceptedGenesis" in res:
                print("genesis already accepted", account.address)
                accepted_genesis = True
            elif "success" in res and "userSummary" in res["success"] and res["success"]["userSummary"] == None:
                print("Not eligible blyaaaaa", account.address)
                acc_res = {"address": account.address, "points": 0, "accepted_genesis": "Not eligible"}
                append_to_csv(acc_res)
                continue
            else:
                print("Error fetching acc points", account.address, res)
                print("Response:", res)
                print("Skip + Sleeping...")
                time.sleep(randint(1, 5))
                continue

            if not accepted_genesis:
                print("Accepting genesis", account.address)
                p = build_tos_payload(account, int(time.time()))
                res = api.post("/info", p)
                if res == "success":
                    print("Genesis accepted", account.address)
                    accepted_genesis = True
                else:
                    print("Error accepting genesis", account.address, res)

            acc_res = {"address": account.address, "points": acc_points, "accepted_genesis": accepted_genesis}
            append_to_csv(acc_res)
            print("Done", account.address)
            total_points += acc_points
            print("Total points fetched so far:", total_points)
            print("Sleeping...")
            time.sleep(randint(1, 5))
        except Exception as e:
            print("Error", e)
            print("Sleeping...")
            time.sleep(randint(1, 5))
            continue