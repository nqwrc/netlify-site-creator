import requests


class NetlifyAPI:
    def __init__(self, access_token):
        self.netlify_api_endpoint = "https://api.netlify.com/api/v1/sites"
        self.headers = self.create_headers(access_token)

    def create_headers(self, access_token):
        """
        Create headers for the API request
        """
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }

    def create_new_site(self, custom_name):
        """
        Create a new site with the given custom URL
        """
        data = {
            'name': custom_name,
            'files': {
                "index.html": "index.html",
                "first.html": "c5045de396718f8bed7d275a5db66889f8ba8fcb",
                "second.html": "60a485665b50c25c0ac83b23417ac588421c6bb6",
                "third.html": "9b780b93bf552555404bc5b13951fa568a005904",
            }
        }
        try:
            response = requests.post(
                self.netlify_api_endpoint, headers=self.headers, json=data)

            if response.status_code != 201:
                raise ValueError(
                    f"Error creating site. Status code: {response.status_code}")
            return custom_name
        except requests.exceptions.RequestException as e:
            print(f"Error creating site: {e}")

    def get_site_id(self, site_name):
        """
        Get the ID of a site based on its name
        :param site_name: name of the site to get ID of
        """
        try:
            response = requests.get(
                self.netlify_api_endpoint, headers=self.headers)
            if response.status_code != 200:
                raise ValueError(
                    f"Error getting site ID. Status code: {response.status_code}")
            sites = response.json()
            for site in sites:
                if site['name'] == site_name:
                    return site['id']
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error getting site ID: {e}")

    def get_all_sites(self):
        """
        Get a list of all the sites that you own
        """
        try:
            response = requests.get(
                self.netlify_api_endpoint, headers=self.headers)

            if response.status_code != 200:
                raise ValueError(
                    f"Error getting all sites. Status code: {response.status_code}")
            sites = [site['name'] for site in response.json()]

            return sites

        except requests.exceptions.RequestException as e:
            print(f"Error getting all sites: {e}")

    def check_site_exists(self, site_name):
        """
        Check if a site that you own with the given name already exists
        """
        try:
            response = requests.get(
                self.netlify_api_endpoint, headers=self.headers)

            if response.status_code != 200:
                raise ValueError(
                    f"Error checking site existence. Status code: {response.status_code}")
            sites = [site['name'] for site in response.json()]
            return site_name in sites
        except requests.exceptions.RequestException as e:
            print(f"Error checking site existence: {e}")

    def create_site(self, custom_name):
        """Create a new site with the given custom URL"""
        if not self.check_site_exists(custom_name):
            print(f"{self.create_new_site(custom_name)} Created successfully!")

    def delete_site(self, site_name):
        """
        Delete an existing site
        :param site_name: name of the site to delete
        """
        try:
            site_id = self.get_site_id(site_name)
            if not site_id:
                raise ValueError(f"Site {site_name} not found.")

            response = requests.delete(
                f"{self.netlify_api_endpoint}/{site_id}", headers=self.headers)

            if response.status_code == 204:
                print(f"{site_name} deleted successfully.")
                return True
            elif response.status_code == 401:
                raise ValueError("Unauthorized. Invalid access token.")
            elif response.status_code == 404:
                raise ValueError(f"Site {site_name} not found.")
            else:
                raise ValueError(f"Error deleting site: {response.content}")
        except requests.exceptions.RequestException as e:
            print(f"Error deleting site: {e}")
            return False
