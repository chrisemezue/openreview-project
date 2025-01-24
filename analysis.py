import openreview
#pip install openreview-py

from tqdm import tqdm
import json


# # API V2
# client = openreview.api.OpenReviewClient(
#     baseurl='https://api2.openreview.net',
#     username='',
#     password=''
# )

# ## get all venues
# venues = client.get_group(id='venues').members
# #venuesl = [v.lower() for v in venues]
# iclr = [v for v in venues if 'ICLR' in v]
# iclr_conf = [v for v in iclr if 'conference' in v]
#breakpoint()
venue_id = 'ICLR.cc/2021/Conference'

# from https://colab.research.google.com/drive/1vXXNxn8lnO3j1dgoidjybbKIN0DW0Bt2#scrollTo=_qmSij2me5bX

guest_client = openreview.Client(baseurl='https://api.openreview.net')
submissions = openreview.tools.iterget_notes(
        guest_client, invitation=f'{venue_id}/-/Blind_Submission')
submissions_by_forum = {n.forum: n for n in submissions}
print('getting metadata...')

invitations = openreview.tools.iterget_invitations(guest_client,regex=f'{venue_id}/')
invites = [inv.id for inv in invitations]

# get all papers
paper_invites = [i for i in invites if 'Paper' in i] # paper invites only have comment and decision
paper_invites = list(set([i.split('-')[0].strip() for i in paper_invites]))
paper_invites_review = [f'{i}-/Official_Review' for i in paper_invites]

paper_anon_reviews_signatures = [[f'{pi}AnonReviewer{id}' for id in range(4)]for pi in paper_invites]
paper_anon_reviews_signatures = [a for m in paper_anon_reviews_signatures for a in m]
breakpoint()


all_reviews = guest_client.get_all_notes(signatures = paper_anon_reviews_signatures)
review_dict= []

for p_inv in tqdm(paper_invites,desc='Parsing reviews'):

    # There should be 3 reviews per forum.
    reviews = openreview.tools.iterget_notes(guest_client, invitation=p_inv)
    reviews2 = openreview.tools.iterget_notes(guest_client, content={'writers' : ['ICLR.cc/2021/Conference']})

    
    for review in reviews:
        review_sample = {}
        
        breakpoint()
        review_sample['forum'] = review.forum

# # API V1
# client = openreview.Client(
#     baseurl='https://api.openreview.net',
#     username=<your username>,
#     password=<your password>
# )



# let's use "iclr.cc/2023/conference"


## how to get all reviews
# https://docs.openreview.net/how-to-guides/data-retrieval-and-modification/how-to-get-all-reviews#venues-using-api-v2



# ## with V2
# venue_group = client.get_group(venue_id)
# submission_name = venue_group.content['submission_name']['value']
# submissions = client.get_all_notes(invitation=f'{venue_id}/-/{submission_name}', details='replies')

# review_name = venue_group.content['review_name']['value']

# reviews=[openreview.api.Note.from_json(reply) for s in submissions for reply in s.details['replies'] if f'{venue_id}/{submission_name}{s.number}/-/{review_name}' in reply['invitations']]


# ## with V1
# submissions = client.get_all_notes(
#     invitation=venue_id,
#     details='directReplies'
# )

# reviews = [] 
# for submission in submissions:
#     reviews = reviews + [openreview.Note.from_json(reply) for reply in submission.details["directReplies"] if reply["invitation"].endswith("Official_Review")]

breakpoint()



"""
title
abstract
review0
rating0
confidence
review1
rating1
decision
"""