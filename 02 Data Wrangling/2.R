df %>% group_by(party) %>% ggplot(aes(x=date, y=facebook, color=party)) + geom_point() + facet_wrap(~party)

