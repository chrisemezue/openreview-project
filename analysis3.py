import json
import openreview

def process_submissions_and_reviews(client, conference_id):
    # Fetch all submissions
    submissions = list(openreview.tools.iterget_notes(client, invitation=f'{conference_id}/-/Blind_Submission'))
    
    # Fetch all reviews
    reviews = list(openreview.tools.iterget_notes(client, invitation=f'{conference_id}/-/Official_Review'))
    
    breakpoint()
    # Organize reviews by paper ID
    review_dict = {}
    for review in reviews:
        paper_id = review.forum  # Forum ID links reviews to submissions
        if paper_id not in review_dict:
            review_dict[paper_id] = []
        review_dict[paper_id].append({
            "review": review.content.get("review", ""),
            "rating": review.content.get("rating", "")
        })

    # Create structured output
    processed_data = []
    for submission in submissions:
        paper_id = submission.id
        paper_data = {
            "title": submission.content.get("title", ""),
            "abstract": submission.content.get("abstract", ""),
            "decision": submission.content.get("decision", ""),
        }

        # Add reviews dynamically
        if paper_id in review_dict:
            for idx, review in enumerate(review_dict[paper_id]):
                paper_data[f"review{idx}"] = review["review"]
                paper_data[f"rating{idx}"] = review["rating"]
        
        processed_data.append(paper_data)

    # Save to JSON file
    with open("processed_reviews.json", "w", encoding="utf-8") as f:
        json.dump(processed_data, f, indent=4, ensure_ascii=False)
    
    print("Processed data saved to processed_reviews.json")

# Usage example (replace with actual OpenReview client and conference ID)
guest_client = openreview.Client(baseurl="https://api.openreview.net")
conference_id = "ICLR.cc/2021/Conference"  # Replace with the actual conference ID

process_submissions_and_reviews(guest_client, conference_id)
