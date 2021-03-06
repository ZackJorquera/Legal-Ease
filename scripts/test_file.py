from summarizer import Summarizer 

with open('sample.txt', encoding="utf8") as text_file:
    
    # Load text
    sample_text = str(text_file.read())
    
    # Remove unwanted text in the essay. ie '(fr)'
    sample_text = sample_text.replace('(fr) ', '')
    
    # Load document class
    summarizer = Summarizer(text=sample_text)
    
    # get summary
    val, summary = summarizer.get_optimal_subset_by_percent_words(.25, ret_as="str")
    
    # Write out summary
    with open('output.txt', 'w+') as w_file:
        w_file.write(summary)
