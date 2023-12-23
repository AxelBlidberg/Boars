library(ggplot2)
library(dplyr)
library(leaps)
library(caret)
library(olsrr)
library(tseries)

df0 <-read.csv("output_0.csv", header = TRUE, sep = ",", colClasses = c("NULL", "NULL", "numeric", "numeric", "numeric","numeric","numeric"))
df1 <-read.csv("output1.csv", header = TRUE, sep = ",", colClasses = c("NULL", "NULL", "numeric", "numeric", "numeric","numeric","numeric"))
df2 <-read.csv("output2.csv", header = TRUE, sep = ",", colClasses = c("NULL", "NULL", "numeric", "numeric", "numeric","numeric","numeric"))
df3 <-read.csv("output3.csv", header = TRUE, sep = ",", colClasses = c("NULL", "NULL", "numeric", "numeric", "numeric","numeric","numeric"))
df4 <-read.csv("output4.csv", header = TRUE, sep = ",", colClasses = c("NULL", "NULL", "numeric", "numeric", "numeric","numeric","numeric"))
df5 <-read.csv("output_1.csv", header = TRUE, sep = ",", colClasses = c("NULL", "NULL", "numeric", "numeric", "numeric","numeric","numeric"))
df6 <-read.csv("output_2.csv", header = TRUE, sep = ",", colClasses = c("NULL", "NULL", "numeric", "numeric", "numeric","numeric","numeric"))
df7 <-read.csv("output_3.csv", header = TRUE, sep = ",", colClasses = c("NULL", "NULL", "numeric", "numeric", "numeric","numeric","numeric"))
df8 <-read.csv("output_4.csv", header = TRUE, sep = ",", colClasses = c("NULL", "NULL", "numeric", "numeric", "numeric","numeric","numeric"))
df9 <-read.csv("output_5.csv", header = TRUE, sep = ",", colClasses = c("NULL", "NULL", "numeric", "numeric", "numeric","numeric","numeric"))
df10 <-read.csv("output_6.csv", header = TRUE, sep = ",",colClasses = c("NULL", "NULL", "numeric", "numeric", "numeric","numeric","numeric"))
df11 <-read.csv("output_7.csv", header = TRUE, sep = ",",colClasses = c("NULL", "NULL", "numeric", "numeric", "numeric","numeric","numeric"))
df12 <-read.csv("output_8.csv", header = TRUE, sep = ",",colClasses = c("NULL", "NULL", "numeric", "numeric", "numeric","numeric","numeric"))
df13 <-read.csv("output_9.csv", header = TRUE, sep = ",",colClasses = c("NULL", "NULL", "numeric", "numeric", "numeric","numeric","numeric"))
df14 <-read.csv("output5.csv", header = TRUE, sep = ",", colClasses = c("NULL", "NULL", "numeric", "numeric", "numeric","numeric","numeric"))

df_list <- list(df0 = df0, df1 = df1, df2 = df2, df3 = df3, df4 = df4,df5=df5, df6=df6, df7=df7, df8=df8, 
                df10=df10,df11=df11,df12= df12, df13=df13,df14=df14)

df_full <- bind_rows(df_list, .id = "Source")

df0_0 <- subset(df_full, bee_types == 0)
df0_1 <- subset(df_full, bee_types == 1)


df0_bee <- df0_0$beeDataHistory
counts <- table(df0_bee)

counts


# Plot using ggplot2 with position = "dodge"
ggplot(combined_df_filtered, aes(x = factor(beeDataHistory), fill = factor(bee_types))) +
  geom_bar(position = "dodge", stat = "count", width = 0.8, aes(group = interaction(bee_types, Source))) +
  labs(title = "Bar Chart of bee_types (0 and 1) by beeDataHistory",
       x = "beeDataHistory", y = "Count",
       fill = "bee_types", group = "Source") +
  scale_fill_manual(values = c("0" = "blue", "1" = "red")) +
  scale_x_discrete(limits = c("1", "2", "3", "4"))


gen <- c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19)
t0 <- c(60,51,20,4,35,32,15,1,36,33,17,1,20,15,8,0,20,18,10,0)
t1 <- c(60,48,0,0,45,26,0,0,63,45,0,0,41,22,0,0,47,34,0,0)

t0 <- t0/6
t1 <- t1/6

# Create a data frame
df <- data.frame(gen, t0, t1)

# Plot using ggplot2
ggplot(df, aes(x = gen)) +
  geom_line(aes(y = t0, color = "Type 0"), size = 1) +
  geom_line(aes(y = t1, color = "Type 1"), size = 1) +
  labs(title = "Line Diagram", x = "Season", y = "Values") +
  scale_color_manual(values = c("Type 0" = "blue", "Type 1" = "red")) +
  scale_x_continuous(breaks = seq(min(gen), max(gen), by = 4), labels = paste("Season", seq(1, 5, by = 1))) +
  theme_minimal()


dfbee <-read.csv("Bee_Values.csv")
dfbee <- subset(dfbee, select = -c(df_sum0, df_sum1,Gen))
dfbee$index <- seq_len(nrow(dfbee))

df_long_dfbee <- reshape2::melt(dfbee, id.vars = "index", variable.name = "variable", value.name = "value")


ggplot(df_long_dfbee, aes(x = index, y = value))+
         geom_boxplot()


ggplot(df_long_dfbee, aes(x = factor(index), y = value, group = index)) +
  geom_boxplot() +
  labs(title = "Boxplots of both types for Each Index", x = "Index", y = "Value") +
  theme_minimal()

ggplot(subset(df_long_dfbee, index == 1 |index == 5 |index == 9 |index == 13|index == 17),
       aes(x = factor(index), y = value, group = index)) +
  geom_boxplot() +
  labs(title = "Boxplots for Every 4th Index", x = "Index", y = "Value") +
  theme_minimal()


df_t0 <- cbind(dfbee[, c('df0_t0', 'df1_t0', 'df2_t0', 'df3_t0', 'df4_t0', 'df5_t0')])
df_t0$index <- seq_len(nrow(df_t0))
df_t1 <- cbind(dfbee[, c('df0_t1', 'df1_t1', 'df2_t1', 'df3_t1', 'df4_t1', 'df5_t1')])
df_t1$index <- seq_len(nrow(df_t1))

df_long_t0 <- reshape2::melt(df_t0, id.vars = "index", variable.name = "variable", value.name = "value")

# Separate 'variable' into 'dataset' and 'type'
df_long_t0 <- transform(df_long_t0, 
                     dataset = gsub("_t[01]", "", variable),
                     type = gsub("df[0-9]_", "", variable))

# Plot using ggplot2
ggplot(df_long_t0, aes(x = index, y = value,color = dataset)) +
  geom_point(size = 3) +
  labs(title = "Scatterplot of t0 with Fill Based on Dataset", x = "Index", y = "Value") +
  theme_minimal()


df_t1 <- cbind(dfbee[, c('df0_t1', 'df1_t1', 'df2_t1', 'df3_t1', 'df4_t1', 'df5_t1')])


BEE_0 <-read.csv("BEE_0.csv", header = TRUE, sep = ",")
BEE_0 <- subset(BEE_0, select = -c(Gen))
BEE_1 <-read.csv("BEE_1.csv", header = TRUE, sep = ",")
BEE_1 <- subset(BEE_1, select = -c(Gen))

BEE_0$index <- seq_len(nrow(BEE_0))
BEE_1$index <- seq_len(nrow(BEE_1))

df_long_BEE_0 <- reshape2::melt(BEE_0, id.vars = "index", variable.name = "variable", value.name = "value")
df_long_BEE_1 <- reshape2::melt(BEE_1, id.vars = "index", variable.name = "variable", value.name = "value")

# Separate 'variable' into 'dataset' and 'type'
df_long_BEE_0 <- transform(df_long_BEE_0, 
                        dataset = gsub("_t[01]", "", variable),
                        type = gsub("df[0-9]_", "", variable))

df_long_BEE_1 <- transform(df_long_BEE_1, 
                           dataset = gsub("_t[01]", "", variable),
                           type = gsub("df[0-9]_", "", variable))

indices_to_keep <- c(1,5,9,13,17)

df_BEE_0 <- df_long_BEE_0 %>% 
  filter(index %in% indices_to_keep) %>%
  mutate(index = factor(index, levels = indices_to_keep, labels = paste("season", 1:5)))

df_BEE_1 <- df_long_BEE_1 %>% 
  filter(index %in% indices_to_keep) %>%
  mutate(index = factor(index, levels = indices_to_keep, labels = paste("season", 1:5)))


ggplot(df_BEE_0, aes(x = index, y = value, color = factor(dataset), group = factor(dataset))) +
  geom_line() +
  labs(title = "Line Plot for Values in Different Data Frames", x = "Index", y = "Value") +
  theme_minimal()

ggplot(df_BEE_1, aes(x = index, y = value, color = factor(dataset), group = factor(dataset))) +
  geom_line() +
  labs(title = "Line Plot for Values in Different Data Frames", x = "Index", y = "Value") +
  theme_minimal()


ggplot(subset(df_BEE_0),aes(x = factor(index), y = value)) +
  geom_boxplot() +
  labs(title = "Distibution of small bees at the beginning of each season (15 simulations)") +
  ylim(0,21) +
  xlab("") + ylab("Number of bees")
  

ggplot(subset(df_BEE_1),
       aes(x = factor(index), y = value, group = index)) +
  geom_boxplot() +
  labs(title = "Distibution of intermediate bees at the beginning of each season (15 simulations)", x = "Index", y = "Value") +
  ylim(0,21)  +
  xlab("") + ylab("Number of bees")

#Kolla om det är en significant skillnad mellan kategorierna, Gör categorical linear regression??



ggplot(subset(df_long_BEE_1, index == 1 |index == 5 |index == 9 |index == 13|index == 17),
       aes(x = factor(index), y = value, group = index)) +
  geom_boxplot() +
  labs(title = "Distibution of intermidate bee, beginning of each season", x = "Index", y = "Value") +
  theme_minimal() +
  ylim(0,21)

combined_df <- rbind(df_long_BEE_0, df_long_BEE_1)
combined_df$index <- factor(combined_df$index)

# Create a single boxplot with facets
ggplot(subset(combined_df, index %in% c(1, 5, 9, 13, 17)),
       aes(x = factor(index), y = value, group = index)) +
  geom_boxplot() +
  facet_wrap(~interaction(variable, index), scales = "free_y") +
  labs(title = "Distribution of bee values at the beginning of each season",
       x = "Index", y = "Value") +
  theme_minimal() +
  ylim(0, 21)



# Plot using ggplot2
ggplot(df_long_BEE_0, aes(x = index, y = value,color = dataset)) +
  geom_point(size = 3) +
  labs(title = "Scatterplot of t0 with Fill Based on Dataset", x = "Index", y = "Value") +
  theme_minimal()


