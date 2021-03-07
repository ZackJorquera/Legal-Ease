from summarizer import Summarizer 

with open('amazon_tos.txt', encoding="utf8") as text_file:
    
    # Load text
    sample_text = str(text_file.read())
    
    # Remove unwanted text in the essay. ie '(fr)'
    sample_text = sample_text.replace('(fr) ', '')
    
    # Load document class
    summarizer = Summarizer(text=sample_text)
    
    # get summary
    val, summary = summarizer.get_optimal_subset_by_percent_words(.5, ret_as="str")
    
    # Write out summary
    with open('output.txt', 'w+') as w_file:
        w_file.write(summary)
        w_file.write(str(val))
