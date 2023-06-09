# KT(korea) mobile carrier plan comparison via fastapi

[![pytest](https://github.com/CodeMath/carrier-plan-comparison-fastapi/actions/workflows/python-app.yml/badge.svg)](https://github.com/CodeMath/carrier-plan-comparison-fastapi/actions/workflows/python-app.yml)

<!-- Pytest Coverage Comment:Begin -->
<a href="https://github.com/CodeMath/carrier-plan-comparison-fastapi/blob/main/README.md"><img alt="Coverage" src="https://img.shields.io/badge/Coverage-89%25-green.svg" /></a><details><summary>Coverage Report </summary><table><tr><th>File</th><th>Stmts</th><th>Miss</th><th>Cover</th><th>Missing</th></tr><tbody><tr><td colspan="5"><b>api/app</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/CodeMath/carrier-plan-comparison-fastapi/blob/main/api/app/dependency.py">dependency.py</a></td><td>6</td><td>6</td><td>0%</td><td><a href="https://github.com/CodeMath/carrier-plan-comparison-fastapi/blob/main/api/app/dependency.py#L1-L10">1&ndash;10</a></td></tr><tr><td colspan="5"><b>api/app/router</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/CodeMath/carrier-plan-comparison-fastapi/blob/main/api/app/router/combination.py">combination.py</a></td><td>95</td><td>7</td><td>93%</td><td><a href="https://github.com/CodeMath/carrier-plan-comparison-fastapi/blob/main/api/app/router/combination.py#L52-L53">52&ndash;53</a>, <a href="https://github.com/CodeMath/carrier-plan-comparison-fastapi/blob/main/api/app/router/combination.py#L125-L126">125&ndash;126</a>, <a href="https://github.com/CodeMath/carrier-plan-comparison-fastapi/blob/main/api/app/router/combination.py#L131-L132">131&ndash;132</a>, <a href="https://github.com/CodeMath/carrier-plan-comparison-fastapi/blob/main/api/app/router/combination.py#L167">167</a></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/CodeMath/carrier-plan-comparison-fastapi/blob/main/api/app/router/plan_list.py">plan_list.py</a></td><td>59</td><td>20</td><td>66%</td><td><a href="https://github.com/CodeMath/carrier-plan-comparison-fastapi/blob/main/api/app/router/plan_list.py#L61">61</a>, <a href="https://github.com/CodeMath/carrier-plan-comparison-fastapi/blob/main/api/app/router/plan_list.py#L63">63</a>, <a href="https://github.com/CodeMath/carrier-plan-comparison-fastapi/blob/main/api/app/router/plan_list.py#L69-L80">69&ndash;80</a>, <a href="https://github.com/CodeMath/carrier-plan-comparison-fastapi/blob/main/api/app/router/plan_list.py#L104">104</a>, <a href="https://github.com/CodeMath/carrier-plan-comparison-fastapi/blob/main/api/app/router/plan_list.py#L112-L122">112&ndash;122</a></td></tr><tr><td><b>TOTAL</b></td><td><b>295</b></td><td><b>33</b></td><td><b>89%</b></td><td>&nbsp;</td></tr></tbody></table></details>
<!-- Pytest Coverage Comment:End -->


## docker build test

```
docek build -t backend carrier:v1 .
docker run --rm -p 9090:8080 carrier:v1
```
check the 0.0.0.0:9090 access. 

***
## docekr compose
```
docker-compose up
```
check 0.0.0.0:8080
