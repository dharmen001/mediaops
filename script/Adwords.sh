#!/usr/bin/env bash
#!/bin/sh
nohup python /home/groupm/mediaops-project/mediaops/Classes/PlatformScript/GetAdwordsCampaign.py
nohup python /home/groupm/mediaops-project/mediaops/Classes/PlatformScript/AdwordsFileReader.py
nohup python /home/groupm/mediaops-project/mediaops/Classes/PlatformScript/RemoveAdwords.py
