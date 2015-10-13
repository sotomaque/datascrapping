# mutate
df <- df %>% select(DATE_, NAME_, PARTY, FACEBOOK, TWITTER) %>% mutate(sum =as.numeric(as.numeric_version(FACEBOOK)) + as.numeric(as.numeric_version(TWITTER))) %>% tbl_df # Equivalent: select cut, clarity, x+y+z as sum from diamonds where ((cut = 'Good' or cut = 'Fair') and clarity = 'VS1') or cut is null

df %>% View()
