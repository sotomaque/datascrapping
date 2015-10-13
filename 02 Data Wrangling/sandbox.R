
# mutate
df <- df %>% select(date, name, party, facebook, twitter) %>% mutate(sum =as.numeric(as.numeric_version(facebook)) + as.numeric(as.numeric_version(twitter))) %>% tbl_df 


df %>% group_by(party) %>% ggplot(aes(x=date, y=sum, color=party)) + geom_point() + facet_wrap(~party)

df %>% mutate(ntile_facebook = ntile(facebook,100)) %>% arrange(desc(ntile_facebook))%>% ggplot(aes(x=date(), y=sum, color=party)) + geom_point() + facet_wrap(~party)

df %>% mutate(ntile_twitter = ntile(twitter,100)) %>% arrange(desc(ntile_twitter)) %>% ggplot(aes(x=date(), y=twitter, color=party)) + geom_point() + facet_wrap(~party)



