/*
 * Copyright (c) 2017, EPAM SYSTEMS INC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.epam.dlab.dto.azure.edge;

import com.epam.dlab.dto.ResourceSysBaseDTO;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.common.base.MoreObjects;

public class EdgeCreateAzure extends ResourceSysBaseDTO<EdgeCreateAzure> {
    @JsonProperty("azure_datalake_enable")
    private String azureDataLakeEnable;
    @JsonProperty("azure_user_name")
    private String azureUserName;

    public EdgeCreateAzure withAzureDataLakeEnable(String azureDataLakeEnable) {
        this.azureDataLakeEnable = azureDataLakeEnable;
        return this;
    }

    public EdgeCreateAzure withAzureUserName(String azureUserName) {
        this.azureUserName = azureUserName;
        return this;
    }

    public String getAzureDataLakeEnable() {
        return azureDataLakeEnable;
    }

    public String getAzureUserName() {
        return azureUserName;
    }


    public void setAzureDataLakeEnable(String azureDataLakeEnable) {
        this.azureDataLakeEnable = azureDataLakeEnable;
    }

    public void setAzureUserName(String azureUserName) {
        this.azureUserName = azureUserName;
    }

    @Override
    public MoreObjects.ToStringHelper toStringHelper(Object self) {
        return super.toStringHelper(this)
                .add("azureDataLakeEnable", azureDataLakeEnable)
                .add("azureUserName", azureUserName);
    }

    @Override
    public String toString() {
        return toStringHelper(this).toString();
    }
}
