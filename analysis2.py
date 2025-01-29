import openreview

# Initialize the OpenReview client
client = openreview.Client(baseurl='https://api.openreview.net')

# Define the ICLR 2021 conference ID
conference_id = 'ICLR.cc/2021/Conference'

# Retrieve all submissions for ICLR 2021
submissions = client.get_all_notes(invitation=f'{conference_id}/-/Blind_Submission', details='directReplies')

# Initialize a list to store reviews
reviews = []

# Iterate through each submission to extract reviews
for submission in submissions:
    # Filter replies to find official reviews
    submission_reviews = [
        openreview.Note.from_json(reply) for reply in submission.details['directReplies']
        if reply['invitation'].endswith('Official_Review')
    ]
    reviews.extend(submission_reviews)

# Output the total number of reviews retrieved
print(f'Total reviews retrieved: {len(reviews)}')

# Example: Print the first review's content
if reviews:
    first_review = reviews[0]
    print(f'Review for paper titled "{first_review.content.get("title", "No Title")}"')
    print(f'Rating: {first_review.content.get("rating", "No Rating")}')
    print(f'Review Content: {first_review.content.get("review", "No Content")}')

    breakpoint()