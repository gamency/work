import h2o
from h2o.automl import H2OAutoML

h2o.init(ip='localhost')

df = h2o.import_file("./prostate.csv")

train, test = df.split_frame(ratios=[.9])

x = train.columns

y = "CAPSULE"

x.remove(y)

train[y] = train[y].asfactor()
test[y] = test[y].asfactor()

aml = H2OAutoML(max_runtime_secs = 60)
aml.train(x = x, y = y, training_frame= train, leaderboard_frame=test)

print(aml.leaderboard)
print(aml.leader)

preds = aml.predict(test)
# preds = aml.leader.predict(test)

print(preds)