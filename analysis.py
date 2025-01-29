import openreview
import json

# Initialize the OpenReview client
client = openreview.Client(baseurl='https://api.openreview.net')



def main(year):
    # Define the ICLR conference ID
    conference_id = f'ICLR.cc/{year}/Conference'

    # Retrieve all submissions for ICLR 2021 with their direct replies
    submissions = client.get_all_notes(
        invitation=f'{conference_id}/-/Blind_Submission',
        details='directReplies'
    )

    # Initialize a list to store the processed data
    processed_data = []

    # Iterate through each submission to extract required information
    for submission in submissions:
        # Initialize a dictionary to store submission details
        submission_data = {
            'title': submission.content.get('title', 'No Title'),
            'abstract': submission.content.get('abstract', 'No Abstract')
        }

        # Initialize counters for reviews and ratings
        review_counter = 0

        # Iterate through direct replies to find reviews and decisions
        for reply in submission.details['directReplies']:
            invitation = reply.get('invitation', '')
            if invitation.endswith('Official_Review'):
                # Extract review content and rating
                review_content = reply['content'].get('review', 'No Review Content')
                rating = reply['content'].get('rating', 'No Rating')

                # Add review and rating to the submission data
                submission_data[f'review{review_counter}'] = review_content
                submission_data[f'rating{review_counter}'] = rating
                review_counter += 1
            elif invitation.endswith('Decision'):
                # Extract decision
                decision = reply['content'].get('decision', 'No Decision')
                submission_data['decision'] = decision

        # Append the processed submission data to the list
        processed_data.append(submission_data)

    # Save the processed data to a JSON file
    with open(f'iclr{year}_reviews.json', 'w') as json_file:
        json.dump(processed_data, json_file, indent=2)

    print(f'Total submissions processed: {len(processed_data)}')

for year in range(2010,2025):
    main(year)