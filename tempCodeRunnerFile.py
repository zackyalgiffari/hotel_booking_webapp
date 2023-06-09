= df['arrival_date_year'].dt.year
    df['cohort_year'] = df.groupby('customer_type')['arrival_date_year'].transform('min')
    df['cohort_index'] = df.groupby('customer_type').cumcount() + 1
    cohort_data = df.groupby(['cohort_year', 'cohort_index'])['is_canceled'].mean().unstack(0)
    fig2 = px.imshow(cohort_da