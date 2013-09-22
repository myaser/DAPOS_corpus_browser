from django import forms


class SearchForm(forms.Form):
    processes = (('concordance', 'Concordance'),
                 ('collocations', 'Collocation'),
                 ('NGram', 'NGram'))

    scoring_algos = (
        ('None', 'Choose...'),
        ('log_likelihood', 'log likelihood'),
        ('mutual_information', 'Mutual Information'),
        ('t-score', 'T-Score'),
    )

    estimators = (
        ('None', 'Choose...'),
        ("MLEEstimator", "maximum likelihood"),
        ("LidstoneEstimator", "add k smoothing"),
        ("LaplaceEstimator", "add one smoothing"),
        ("ELEEstimator", "expected estimation"),
        ("UnigramPriorEstimator", "unigram prior"),
    )

    search_phrase = forms.CharField(max_length=100, required=False)
    process = forms.ChoiceField(choices=processes, required=False)
    collocation_algorithm = forms.ChoiceField(choices=scoring_algos, required=True)
    ngram_size = forms.IntegerField(min_value=1, max_value=5, required=True)
    ngram_estimator = forms.ChoiceField(choices=estimators, required=True)

    def clean(self, *args, **kwargs):
        cleaned_data = super(SearchForm, self).clean(*args, **kwargs)
        if cleaned_data.get('process') == 'collocations':
            if not cleaned_data.get('collocation_algorithm'):
                raise forms.ValidationError(
                    'You should choose collocation scoring algorithm')
        elif cleaned_data.get('process') == 'NGram':
            if not cleaned_data.get('ngram_size'):
                raise forms.ValidationError('You should set ngram size')
            if not cleaned_data.get('ngram_estimator'):
                raise forms.ValidationError(
                    'You should choose the estimation method')

        return cleaned_data
