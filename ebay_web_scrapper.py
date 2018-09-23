"""
This program take user keywords, search them on Ebay.com
and import into a CSV files product names, prices,
shipping costs and links to its description.

"""
import math
from urllib.request import urlopen as uOp
from bs4 import BeautifulSoup as soup


def main():
    """
    Main function:
    ->Takes user keywords and check its results on Ebay.com
    ->File management
    ->Verbose
    """
    print("What do you want to search on Ebay ?")
    search_item = input()
    print("[*]Searching \""+str(search_item)+"\".")
    search_item = search_item.strip()
    search_item = search_item.replace(" ", "+")
    url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw="+str(search_item)+"&_sacat=0&_ipg=200"
    print("[*]Requesting URL: '"+str(url)+"'.")


    tree = request(url)
    nb_pages = pages(tree)
    print("[*]Checking page.")
    if int(nb_pages) == 0:
        print("[-]0 item found, exit...")
        exit()

    else:
        input("[+]"+str(nb_pages)+ " Pages to process. Press Enter to continue.(ctrl + c to quit)")
        filename_item = search_item.title().replace("+", "_")
        filename = "Ebay_"+str(filename_item)+".csv"
        try:
            fopen = open(filename, "x")
            print("[*]Creating file "+str(filename)+".")
        except:
            user_input = input("[-]"+ filename + " already exist, overwrite [y/n] ?\n")
            answer = yes_no(user_input)

            if answer is True:
                print("[*]Overwriting "+filename+".")
                fopen = open(filename, "w")
                headers = "Product_name, Price, Shipping , Link_to_Description \n"
                print("[*]Adding headers: "+str(headers.replace("\n", "")))
                fopen.write(headers)
            elif answer is False:
                print("[*]Appending "+filename+".")
                fopen = open(filename, "a")

        x = 1
        while x <= nb_pages:
            print("[*]Scraping items from page "+str(x)+".")
            new_url = url + "&_pgn="+str(x)
            new_tree = request(new_url)
            item = new_tree.findAll("div", {"class":"s-item__wrapper"})
            extract(item, filename)
            x += 1
        else:
            print("[+]Done. No more pages to process.")

    fopen.close()


def yes_no(answer):
    """
    -> Manages Yes-No question
    """
    yes = set(['yes', 'y', 'ye'])
    no = set(['no', 'n'])
    choice = answer.lower()
    while True:

        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print("Please respond with 'yes' or 'no'")
            choice = input().lower()



def pages(tree):
    """
    -> Checks nb of items found and nb of pages to process (using a layout of 200 items/page)
    """
    nb_item = tree.findAll("h1", {"class":"srp-controls__count-heading"})
    nb_item = nb_item[0].text.replace("results", "")
    nb_item = nb_item.replace(",", "").strip()
    nb_pages = math.ceil(int(nb_item)/ 200)
    return nb_pages



def request(url):
    """
    -> Request URL and "soups" it
    """
    try:
        url_client = uOp(url)
        raw_html = url_client.read()
        url_client.close()
        soup_html = soup(raw_html, "html.parser")
        return soup_html
    except Exception as exc:
        print("[-]Error: "+str(exc)+" ,exit...")
        exit()


def extract(item, file_name):
    """
    -> Extract items Name, link, price and shipping cost and write it into the CSV file
    """
    for container in item:
    #grab the title of the item
        print("               ----------------------------------------------")
        title_ref = container.findAll("h3", {"class":"s-item__title"})
        title = title_ref[0].text.strip()
        print("[+] "+str(title)+".")

        container_link_ref = container.findAll("a", {"class":"s-item__link"})
        link = container_link_ref[0].get("href")


    #grab the price of the item
        price_ref = container.findAll("span", {"class":"s-item__price"})
        price = price_ref[0].text.strip()
        print("[+] "+str(price)+".")

    #grab the shipping cost
        try:
            shipping_ref = container.findAll("span", {"class":"s-item__shipping s-item__logisticsCost"})
            shipping = shipping_ref[0].text.strip()
            print("[+] "+str(shipping)+".")
            with open(file_name, "a+") as fopen:
                fopen.write(title.replace(",", " ")+ ","+price.replace(",", ".")+","+shipping.replace(",", ".")+","+link+"\n")
        except:
            with open(file_name, "a+") as fopen:
                fopen.write(title.replace(",", " ")+","+price.replace(",", ".")+",None,"+link+"\n")
                continue


main()
