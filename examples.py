from NetlifySiteManager import NetlifyAPI

if __name__ == "__main__":
    # Insert your token as variable
    access_token = 'YOUR_ACCESS_TOKEN'

    # Create instance of NetlifyAPI
    netlify = NetlifyAPI(access_token)

    # Create a site : https://example.netlify.app/
    netlify.create_site('example')

    # List all the sites you own
    sites = netlify.get_all_sites()
    for s in sites:
        print(sites)

    # Delete a site : https://example.netlify.app/
    netlify.delete_site('example')
