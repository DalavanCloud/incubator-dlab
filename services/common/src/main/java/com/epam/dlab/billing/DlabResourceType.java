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

package com.epam.dlab.billing;

import com.google.common.collect.Lists;

import java.util.ArrayList;
import java.util.List;

public enum DlabResourceType {
    SSN,
    SSN_BUCKET,
    SSN_CONTAINER,
    COLLABORATION_BUCKET,
    COLLABORATION_CONTAINER,
    EDGE,
    EDGE_BUCKET,
    EDGE_CONTAINER,
    EXPLORATORY,
    COMPUTATIONAL;

    public static DlabResourceType of(String string) {
        if (string != null) {
            for (DlabResourceType value : DlabResourceType.values()) {
                if (string.equalsIgnoreCase(value.toString())) {
                    return value;
                }
            }
        }
        return null;
    }

    public static String getResourceTypeName(String id) {
        DlabResourceType resourceTypeId = DlabResourceType.of(id);
        if (resourceTypeId != null) {
            switch (resourceTypeId) {
                case COMPUTATIONAL:
                    return "Cluster";
                case EXPLORATORY:
                    return "Notebook";
                case EDGE:
                    return "Edge Node";
                case EDGE_BUCKET:
                case SSN_BUCKET:
                case COLLABORATION_BUCKET:
                    return "Bucket";
                case EDGE_CONTAINER:
                case SSN_CONTAINER:
                case COLLABORATION_CONTAINER:
                    return "Container";
                case SSN:
                    return "SSN";
            }
        }
        return id;
    }

    public static List<String> getResourceTypeIds(List<String> names) {
        if (names == null || names.isEmpty()) {
            return Lists.newArrayList();
        }

        List<String> list = new ArrayList<>();
        names.forEach(e -> {
            switch (e) {
                case "Cluster":
                    list.add(DlabResourceType.COMPUTATIONAL.toString());
                    break;
                case "Notebook":
                    list.add(DlabResourceType.EXPLORATORY.toString());
                    break;
                case "Edge Node":
                    list.add(DlabResourceType.EDGE.toString());
                    break;
                case "Bucket":
                    list.add(DlabResourceType.EDGE_BUCKET.toString());
                    list.add(DlabResourceType.SSN_BUCKET.toString());
                    list.add(DlabResourceType.COLLABORATION_BUCKET.toString());
                    break;
                case "Container":
                    list.add(DlabResourceType.EDGE_CONTAINER.toString());
                    list.add(DlabResourceType.SSN_CONTAINER.toString());
                    list.add(DlabResourceType.COLLABORATION_CONTAINER.toString());
                    break;
                case "SSN":
                    list.add(DlabResourceType.SSN.toString());
                    break;
                default:
                    list.add(e);
            }
        });

        return list;
    }

    @Override
    public String toString() {
        return super.toString().toUpperCase();
    }
}
