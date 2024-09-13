import requests
from django.core.management.base import BaseCommand
from tokens.models import *  # Adjust the import according to your actual model and app names

class Command(BaseCommand):
    help = 'Fetch and store newly launched tokens on the Tron blockchain'

    def handle(self, *args, **kwargs):
        api_url = 'https://apilist.tronscan.org/api/token'  # Replace with the correct API URL if different
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            tokens_data = response.json()  # Assuming the API returns JSON data

            # Sort tokens by dateCreated in descending order (newest first)
            sorted_tokens = sorted(tokens_data.get('data', []), key=lambda x: x.get('dateCreated', 0), reverse=True)

            for token_data in sorted_tokens:
                token_id = token_data.get('tokenID')  # Use tokenID as the unique identifier
                
                if not token_id:
                    self.stdout.write(self.style.WARNING(f'Skipping token without tokenID: {token_data.get("name", "Unknown")}'))
                    continue

                token, created = Token.objects.update_or_create(
                    identifier=token_id,  # Use tokenID as the unique identifier
                    defaults={
                        'name': token_data.get('name', 'Unknown'),
                        'symbol': token_data.get('abbr', 'Unknown'),  # Assuming 'abbr' is the symbol
                        'decimals': token_data.get('precision', 0),  # Assuming 'precision' is the number of decimals
                        'total_supply': token_data.get('totalSupply', '0'),  # Assuming 'totalSupply' is the total supply
                        'description': token_data.get('description', ''),  # Include description if available
                        'website': token_data.get('website', ''),  # Include website if available
                        'img_url': token_data.get('imgUrl', ''),  # Include image URL if available
                        # Add other fields as necessary
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created token: {token.name}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated token: {token.name}'))

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Error fetching tokens: {e}'))
        except ValueError as e:
            self.stderr.write(self.style.ERROR(f'Error parsing JSON response: {e}'))

