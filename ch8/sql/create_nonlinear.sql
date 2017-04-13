

PASSWORD=pwd:Packt17 psql -h amlpackt.cenllwot8v9r.us-east-1.redshift.amazonaws.com -p 5439 -U alexperrier -d amlpacktdb

> export REDSHIFT_CONNECT='-h amlpackt.cenllwot8v9r.us-east-1.redshift.amazonaws.com -p 5439 -U alexperrier -d amlpacktdb'


CREATE TABLE IF NOT EXISTS nonlinear (
    x     real,
    y      real
);


# import nonlinear csv into amlpacktdb.nonlinear
upload csv to s3
> aws s3 cp data/nonlinear.csv s3://aml.packt/data/ch9/

copy nonlinear from 's3://aml.packt/data/ch9/nonlinear.csv' CREDENTIALS 'aws_access_key_id=AKIAII7IZQ6QQVBGVHLA;aws_secret_access_key=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' CSV;

> INFO:  Load into table 'nonlinear' completed, 1000 record(s) loaded successfully.

psql $REDSHIFT_CONNECT -c "select count(*) from nonlinear"
Pager usage is off.
Timing is on.
 count
-------
  1000
(1 row)

Time: 32.391 ms




