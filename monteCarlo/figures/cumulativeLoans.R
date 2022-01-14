#library(tibble)
library(ggplot2)

loans = read.table("core_data.csv", header = TRUE, sep = ',')
model = read.table("model_predictions.csv", header = TRUE, sep = ',')


loans$model = model$model

plot = ggplot(loans, aes(x=period, y=model))+
    geom_ribbon(aes(period, ymax=maximum, ymin=minimum), fill="gray", alpha = 0.25)+
    geom_line(aes(period, model))+
    geom_line(aes(period, naive))+
    geom_point(aes(period, model), size = 3)+
    geom_point(aes(period, naive), shape="triangle", size = 3)+
    theme_bw()

